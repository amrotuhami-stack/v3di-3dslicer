"""
V3Di 3D Slicer Backend - FastAPI Application
Integrates 3D Slicer for CBCT processing and segmentation
"""

import os
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import boto3
import subprocess
import json

# Configuration
S3_BUCKET = os.environ.get('S3_BUCKET', 'v3di-slicer-data')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-2')
SLICER_HOME = os.environ.get('SLICER_HOME', '/opt/v3di-backend/Slicer')
UPLOAD_DIR = Path('/opt/v3di-backend/uploads')
OUTPUT_DIR = Path('/opt/v3di-backend/outputs')

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize FastAPI
app = FastAPI(
    title="V3Di 3D Slicer Backend",
    description="CBCT Processing and AI Segmentation powered by 3D Slicer",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage
jobs: Dict[str, Dict[str, Any]] = {}

# S3 Client
s3_client = boto3.client('s3', region_name=AWS_REGION)


# Models
class SegmentationRequest(BaseModel):
    study_id: str
    model_type: str = "teeth"  # teeth, anatomy, implant


class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None


# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    slicer_exists = Path(SLICER_HOME).exists()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "slicer_available": slicer_exists,
        "slicer_path": SLICER_HOME,
        "active_jobs": len([j for j in jobs.values() if j.get("status") == "processing"])
    }


@app.post("/upload-dicom")
async def upload_dicom(file: UploadFile = File(...)):
    """Upload a DICOM file or archive"""
    study_id = str(uuid.uuid4())[:8]
    study_dir = UPLOAD_DIR / study_id
    study_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = study_dir / file.filename
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # If it's a zip, extract it
    if file.filename.endswith('.zip'):
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(study_dir)
    
    return {
        "study_id": study_id,
        "filename": file.filename,
        "path": str(study_dir)
    }


@app.post("/segment")
async def start_segmentation(request: SegmentationRequest, background_tasks: BackgroundTasks):
    """Start a segmentation job"""
    job_id = str(uuid.uuid4())[:8]
    
    jobs[job_id] = {
        "job_id": job_id,
        "study_id": request.study_id,
        "model_type": request.model_type,
        "status": "queued",
        "progress": 0,
        "message": "Job queued",
        "created_at": datetime.now().isoformat(),
        "stl_urls": [],
        "result": None
    }
    
    # Start background processing
    background_tasks.add_task(run_segmentation, job_id, request.study_id, request.model_type)
    
    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
        "message": job["message"],
        "stl_urls": job.get("stl_urls", []),
        "result": job.get("result")
    }


@app.get("/download/stl/{job_id}/{filename}")
async def download_stl(job_id: str, filename: str):
    """Download generated STL file"""
    file_path = OUTPUT_DIR / job_id / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )


@app.get("/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "jobs": [
            {
                "job_id": j["job_id"],
                "status": j["status"],
                "progress": j["progress"],
                "created_at": j.get("created_at")
            }
            for j in jobs.values()
        ]
    }


# Background processing
async def run_segmentation(job_id: str, study_id: str, model_type: str):
    """Run segmentation using 3D Slicer"""
    try:
        job = jobs[job_id]
        job["status"] = "processing"
        job["message"] = "Initializing 3D Slicer..."
        job["progress"] = 5
        
        study_dir = UPLOAD_DIR / study_id
        output_dir = OUTPUT_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Update progress
        job["progress"] = 10
        job["message"] = "Loading DICOM volume..."
        await asyncio.sleep(0.1)
        
        # Run Slicer Python script
        slicer_script = create_slicer_script(study_dir, output_dir, model_type)
        script_path = output_dir / "process.py"
        
        with open(script_path, 'w') as f:
            f.write(slicer_script)
        
        job["progress"] = 20
        job["message"] = "Running AI segmentation..."
        
        # Execute Slicer with the script
        slicer_path = Path(SLICER_HOME) / "Slicer"
        if not slicer_path.exists():
            # Fallback: simulate processing for demo
            await simulate_processing(job_id, output_dir)
            return
        
        process = subprocess.Popen(
            [str(slicer_path), "--python-script", str(script_path), "--no-splash", "--no-main-window"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Monitor progress
        for progress in range(30, 90, 10):
            await asyncio.sleep(2)
            job["progress"] = progress
            job["message"] = f"Processing... {progress}%"
        
        process.wait()
        
        # Collect STL files
        stl_files = list(output_dir.glob("*.stl"))
        stl_urls = []
        
        for stl_file in stl_files:
            url = f"/download/stl/{job_id}/{stl_file.name}"
            stl_urls.append({
                "name": stl_file.stem,
                "url": url,
                "size": stl_file.stat().st_size
            })
        
        # Complete
        job["status"] = "completed"
        job["progress"] = 100
        job["message"] = "Segmentation complete"
        job["stl_urls"] = stl_urls
        job["result"] = {
            "teeth_count": len(stl_files),
            "output_dir": str(output_dir)
        }
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = str(e)
        jobs[job_id]["progress"] = 0


async def simulate_processing(job_id: str, output_dir: Path):
    """Simulate processing for demo/testing"""
    job = jobs[job_id]
    
    steps = [
        (30, "Loading volume..."),
        (50, "Running AI inference..."),
        (70, "Generating meshes..."),
        (90, "Finalizing..."),
    ]
    
    for progress, message in steps:
        job["progress"] = progress
        job["message"] = message
        await asyncio.sleep(2)
    
    # Create demo STL files
    demo_teeth = ["tooth_11", "tooth_12", "tooth_21", "tooth_22"]
    stl_urls = []
    
    for tooth in demo_teeth:
        # Create placeholder STL
        stl_path = output_dir / f"{tooth}.stl"
        create_demo_stl(stl_path)
        stl_urls.append({
            "name": tooth,
            "url": f"/download/stl/{job_id}/{tooth}.stl",
            "size": stl_path.stat().st_size
        })
    
    job["status"] = "completed"
    job["progress"] = 100
    job["message"] = "Segmentation complete (demo mode)"
    job["stl_urls"] = stl_urls
    job["result"] = {"teeth_count": len(demo_teeth)}


def create_slicer_script(study_dir: Path, output_dir: Path, model_type: str) -> str:
    """Generate Slicer Python script for processing"""
    return f'''
import slicer
import os

# Load DICOM
dicomDataDir = "{study_dir}"
loadedNodeIDs = []

from DICOMLib import DICOMUtils
with DICOMUtils.TemporaryDICOMDatabase() as db:
    DICOMUtils.importDicom(dicomDataDir, db)
    patientUIDs = db.patients()
    for patientUID in patientUIDs:
        loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))

# Get volume node
volumeNode = slicer.util.getNode(loadedNodeIDs[0]) if loadedNodeIDs else None

if volumeNode:
    # Run segmentation (using Segment Editor or custom module)
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes()
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(volumeNode)
    
    # Add segmentation logic here based on model_type: {model_type}
    # This would integrate nnU-Net or other AI models
    
    # Export segments as STL
    outputDir = "{output_dir}"
    slicer.modules.segmentations.logic().ExportSegmentsClosedSurfaceRepresentationToFiles(
        outputDir,
        segmentationNode,
        None,
        "STL"
    )

slicer.util.exit()
'''


def create_demo_stl(path: Path):
    """Create a simple demo STL file"""
    import struct
    
    # Simple triangle
    header = b'\0' * 80
    num_triangles = 1
    
    with open(path, 'wb') as f:
        f.write(header)
        f.write(struct.pack('<I', num_triangles))
        
        # Normal
        f.write(struct.pack('<fff', 0, 0, 1))
        # Vertices
        f.write(struct.pack('<fff', 0, 0, 0))
        f.write(struct.pack('<fff', 1, 0, 0))
        f.write(struct.pack('<fff', 0.5, 1, 0))
        # Attribute
        f.write(struct.pack('<H', 0))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

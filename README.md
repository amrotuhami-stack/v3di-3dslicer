# V3Di 3D Slicer

Dental imaging platform powered by 3D Slicer with Vue.js frontend.

## Architecture

```
┌─────────────────────────────────────┐
│        Firebase Hosting             │
│   Vue.js Frontend (DentaVision)     │
└──────────────────┬──────────────────┘
                   │ HTTPS
                   ▼
┌─────────────────────────────────────┐
│        AWS EC2 (g4dn.xlarge)        │
│   3D Slicer + FastAPI Backend       │
│   nnU-Net / MONAI Segmentation      │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│            AWS S3                   │
│   DICOM, STL, Model Weights         │
└─────────────────────────────────────┘
```

## Frontend

- **Framework**: Vue.js 3 + Vite
- **Theme**: DentaVision (Dark slate/indigo)
- **Hosting**: Firebase (https://v3di-3dslicer.web.app)

### Development

```bash
cd frontend
npm install
npm run dev
```

### Deploy to Firebase

```bash
npm run build
firebase deploy --only hosting
```

## Backend

- **Platform**: AWS EC2 g4dn.xlarge (T4 GPU)
- **Processing**: 3D Slicer (headless mode)
- **API**: FastAPI + uvicorn
- **AI**: nnU-Net v2, MONAI

### Setup on EC2

```bash
cd infrastructure
chmod +x setup_ec2.sh
./setup_ec2.sh
```

### Start Server

```bash
./start_server.sh
```

### API Endpoints

| Endpoint                        | Method | Description        |
| ------------------------------- | ------ | ------------------ |
| `/health`                       | GET    | Health check       |
| `/upload-dicom`                 | POST   | Upload DICOM       |
| `/segment`                      | POST   | Start segmentation |
| `/status/{job_id}`              | GET    | Job status         |
| `/download/stl/{job_id}/{file}` | GET    | Download STL       |

## Project Structure

```
v3di-3dslicer/
├── src/                  # Vue.js frontend
│   ├── assets/          # DentaVision theme
│   ├── components/      # Vue components
│   ├── views/           # Page views
│   ├── stores/          # Pinia stores
│   └── services/        # API services
├── backend/             # Python backend
│   ├── api/            # FastAPI app
│   └── requirements.txt
├── infrastructure/      # AWS setup scripts
└── firebase.json        # Firebase config
```

## License

Proprietary - Voxel3DI

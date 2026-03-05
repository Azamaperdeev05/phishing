# Contributing

Үлестеріңізге рахмет. PR жібермес бұрын төмендегіні сақтаңыз.

## Даму ортасы

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
```

### Frontend

```bash
cd frontend
npm install
npm run lint
npm run build
```

## PR талаптары

- Өзгеріс мақсаты түсінікті болуы керек
- Қатысты тесттер өтуі керек
- Құжаттама (README/API/docs) қажет болса жаңартылуы керек
- Үлкен өзгерістерге қысқа migration notes қосылуы керек

## Commit форматы (ұсыныс)

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `refactor: ...`
- `test: ...`

## Code style

- Backend: қарапайым, анық Python код
- Frontend: TypeScript strict, lint clean
- Қауіпсіздікке қатысты өзгерістерде тәуекелді қысқаша сипаттаңыз


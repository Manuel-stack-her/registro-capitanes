# Registro de Capitanes - Escaneo de Códigos QR

Este proyecto permite registrar las visitas de capitanes a las mesas de una sucursal escaneando códigos QR. Cada visita incluye: el nombre del capitán, el dato del QR (como "TENAYUCA MESA 1"), la fecha y la hora.

## 🚀 Funcionalidades

- Acceso por clave de sucursal.
- Escaneo de códigos QR desde cámara web o móvil.
- Registro automático de la visita con hora y fecha.
- Exportación de registros a **Excel** (.xlsx) y **PDF**.
- Historial visible por fecha y sucursal.
- Gestión de capitanes por sucursal.

## 📦 Requisitos

- Python 3.8+
- Flask
- pandas
- openpyxl
- fpdf

Instalar dependencias:
```bash
pip install flask pandas openpyxl fpdf

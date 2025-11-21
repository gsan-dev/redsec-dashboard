# RedSec Dashboard - Nmap Installation Guide

## ¿Por qué necesitas nmap?

Nmap es una herramienta profesional de escaneo de red que proporciona:
- ✅ Detección precisa de dispositivos activos
- ✅ Identificación de sistema operativo
- ✅ Detección de puertos abiertos
- ✅ Información de fabricante (MAC vendor)
- ✅ Resolución de nombres de host

## Instalación en Windows

### Opción 1: Instalador Manual (Recomendado)

1. **Descarga nmap:**
   - Ve a: https://nmap.org/download.html
   - Descarga: "Latest stable release self-installer" (Windows)
   - Archivo: `nmap-X.XX-setup.exe`

2. **Instala nmap:**
   - Ejecuta el instalador descargado
   - **IMPORTANTE:** Marca la opción "Add Nmap to PATH"
   - Completa la instalación

3. **Verifica la instalación:**
   ```powershell
   nmap --version
   ```
   Deberías ver algo como:
   ```
   Nmap version 7.94 ( https://nmap.org )
   ```

### Opción 2: Con winget

Si tienes winget instalado:
```powershell
winget install Insecure.Nmap
```

## Después de instalar

1. **Reinicia PowerShell/Terminal** (cerrar y abrir de nuevo)

2. **Verifica que funciona:**
   ```powershell
   nmap --version
   ```

3. **Reinicia RedSec Dashboard:**
   - Detén backend y frontend (Ctrl+C)
   - Ejecuta nuevamente: `.\start.ps1`

## Uso del Scanner

Una vez instalado nmap, el scanner detectará automáticamente:

- 📍 **IP Address** de cada dispositivo
- 🏷️ **Hostname** si está disponible
- 🔧 **MAC Address** 
- 🏭 **Vendor** (fabricante del dispositivo)
- 💻 **OS Detection** (requiere ejecutar como administrador)
- 🔌 **Open Ports** (en scans de puertos)

## Ejecutar con privilegios elevados (Opcional)

Para obtener información completa (OS detection, etc.):

1. Abre PowerShell como **Administrador**
2. Navega al proyecto:
   ```powershell
   cd C:\Users\gdev\Desktop\redlab
   ```
3. Inicia el backend:
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Troubleshooting

**Error: "nmap: command not found"**
- Nmap no está en el PATH
- Reinstala y asegúrate de marcar "Add to PATH"
- Reinicia la terminal

**Scan muy lento:**
- Normal para scans completos (30-60 segundos)
- Es mucho más preciso que ping simple

**No detecta OS:**
- Necesitas ejecutar como Administrador
- El scanner funcionará sin esto, solo no mostrará el OS

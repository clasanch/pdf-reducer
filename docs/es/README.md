[English](../../README.md) | [Español](#)  

# PDF Reducer 
Herramienta para reducir el tamaño de archivos PDF usando Ghostscript con procesamiento en paralelo. Básicamente es un wrapper de Ghostscript en paralelo.

## Resumen
Esta herramienta divide un archivo PDF en segmentos, reduce el tamaño de cada segmento usando Ghostscript, y luego combina los segmentos reducidos en un único archivo PDF optimizado. Diseñada para usuarios avanzados que priorizan la velocidad sin sacrificar la legibilidad básica.

## Características Principales
- **Procesamiento en Paralelo:** Divide y reduce segmentos de PDF simultáneamente para acelerar el proceso.
- **Optimización de Imágenes:** Reduce la resolución de imágenes para minimizar el tamaño del archivo.
- **Soporte para Archivos Grandes:** Diseñado para manejar archivos PDF de gran tamaño.
- **Limpieza Automática:** Elimina automáticamente los archivos temporales generados durante el proceso.

## Requisitos
- Python 3.6 o posterior
- [Ghostscript](https://www.ghostscript.com/) instalado en el sistema (herramienta de línea de comandos **gs**)
- PyPDF2 (se instala automáticamente con `pip install -r requirements.txt`)

## Instalación
1. Clona el repositorio:
```bash
git clone https://github.com/clasanch/pdf-reducer.git
cd pdf-reducer
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso
La herramienta se ejecuta desde la línea de comandos:
```bash
python main.py input.pdf -o output.pdf --chunk-size 10 --processes 4
```

### Parámetros
```bash
input.pdf: Archivo PDF de entrada (requerido)
-o/--output: Nombre del archivo PDF de salida (por defecto: reduced_final_file.pdf)
--chunk-size: Número de páginas por segmento (por defecto: 10)
--processes: Número de procesos en paralelo (por defecto: 4)
```

### Ejemplo de Uso
```bash
python main.py documento_grande.pdf -o documento_optimizado.pdf --chunk-size 5 --processes 2
```

### Resultados Esperados
Un archivo PDF optimizado con tamaño significativamente reducido.
Los archivos temporales de segmentos se eliminan automáticamente al finalizar el proceso.

## Limitaciones
Requiere que Ghostscript esté instalado y accesible en el sistema.
No es compatible con PDFs protegidos por contraseña o DRM.
La reducción del tamaño puede afectar la calidad de las imágenes.

## Por Qué Desarrollé Esto
A pesar de usar una MacBook potente, no pude encontrar herramientas gratuitas de reducción de PDF que aprovecharan adecuadamente los procesadores multi-núcleo modernos. Las soluciones existentes tardaban horas en procesar archivos grandes - este script reduce ese tiempo de toda una noche a minutos mientras mantiene una calidad utilizable.

## 📜 Reconocimiento
Este proyecto utiliza componentes de terceros:
- **[PyPDF2](https://github.com/py-pdf/pypdf)** © Mathieu Fenniak et al. (Licencia BSD 3-Cláusulas)
- Requiere **[Ghostscript](https://www.ghostscript.com/)** (Licencia AGPLv3)
Consulta [LICENSES.md](../../LICENSES.md) para ver los detalles completos de las licencias.
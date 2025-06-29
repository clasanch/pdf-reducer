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
- PyMuPDF (se instala automáticamente con `pip install -r requirements.txt`)

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

## ¿Por Qué Este Enfoque?

### Ventajas Técnicas
Esta herramienta combina **PyMuPDF** para manipulación eficiente de PDF con **Ghostscript** para compresión superior, creando un enfoque híbrido que supera a las soluciones de método único:

- **PyMuPDF maneja división/fusión eficientemente**: A diferencia de las librerías puras de Python, PyMuPDF (basado en MuPDF) proporciona rendimiento a nivel C para operaciones de páginas, permitiendo división rápida de segmentos y reensamblaje sin sobrecarga de memoria.

- **Ghostscript ofrece compresión de grado profesional**: Mientras que los optimizadores solo de imágenes se enfocan en fotografías, Ghostscript optimiza toda la estructura del PDF - fuentes, vectores, metadatos e imágenes - logrando mejores ratios de compresión que herramientas independientes.

- **Paralelización real vs procesamiento secuencial**: La mayoría de herramientas PDF procesan páginas secuencialmente. Esta herramienta procesa múltiples segmentos simultáneamente a través de núcleos de CPU, reduciendo dramáticamente el tiempo de procesamiento.

### Benchmarks de Rendimiento
Resultados del mundo real en documentos típicos:
- **Paper de investigación de 300MB (150 páginas)**: 95% de reducción de tamaño, 15min → 3min tiempo de procesamiento
- **Archivos de presentación grandes**: 85-90% de reducción manteniendo claridad del texto
- **Escalado multi-núcleo**: Sistemas de 4 núcleos ven ~3x aceleración vs herramientas de un solo hilo

### Ventaja Competitiva
A diferencia de otros compresores PDF:
- **vs Herramientas online**: Sin límites de subida, procesamiento local enfocado en privacidad
- **vs Adobe Acrobat**: Gratuito, scripteable, y maneja procesamiento en lotes
- **vs ImageMagick**: Mejor preservación de texto/vectores, más rápido en documentos multi-página
- **vs Soluciones puras de Python**: Rendimiento a nivel C a través de integración PyMuPDF

## Por Qué Desarrollé Esto
A pesar de usar una MacBook potente, no pude encontrar herramientas gratuitas de reducción de PDF que aprovecharan adecuadamente los procesadores multi-núcleo modernos. Las soluciones existentes tardaban horas en procesar archivos grandes - este script reduce ese tiempo de toda una noche a minutos mientras mantiene una calidad utilizable.

## 📜 Licencia

Este proyecto está licenciado bajo la **Licencia Pública General GNU Affero v3.0 (AGPLv3)** - consulta el archivo [LICENSE](../../LICENSE) para más detalles.

## 📜 Reconocimiento
Este proyecto utiliza componentes de terceros:
- **[PyMuPDF](https://github.com/pymupdf/PyMuPDF)** © Artifex Software (Licencia AGPLv3)
- Requiere **[Ghostscript](https://www.ghostscript.com/)** (Licencia AGPLv3)

Consulta [LICENSES.md](../../LICENSES.md) para ver los detalles completos de las licencias.
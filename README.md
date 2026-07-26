# Maquinarias Sanlúcar — demo web

Landing responsive para **Maquinarias Sanlúcar**, centrada exclusivamente en maquinaria de obra pública y construcción.

## Vista local

No requiere compilación ni dependencias. Desde la raíz del proyecto:

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000`.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas comprueban estructura, enlaces, assets, límites editoriales de imagen, etiqueta de disponibilidad y ausencia de afirmaciones no permitidas.

## Archivos

- `index.html`: contenido y estructura accesible.
- `styles.css`: diseño responsive, con hero limitado a 1280 px y miniaturas sin ampliación por encima de 308 px.
- `script.js`: menú móvil, cabecera y año del pie.
- `image-sources.json`: procedencia y restricciones editoriales.
- `assets/`: seis recursos aprobados.

## Nota editorial

Las imágenes proceden de perfiles comerciales inequívocos de la empresa y se emplean solo en esta demo. No constituyen inventario ni representan disponibilidad actual. Los derechos no se han declarado como licencia libre; debe confirmarse el permiso de reutilización antes de publicar.

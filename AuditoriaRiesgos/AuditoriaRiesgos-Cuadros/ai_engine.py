from datetime import datetime

def analyze_asset(asset: dict) -> dict:
    """
    Genera un análisis simple (IA local basada en reglas/plantillas)
    Devuelve dict con: evidencia, condicion, recomendacion, riesgo, impacto, controles_iso
    """
    name = asset.get('name', 'Activo sin nombre')
    typ = asset.get('type', 'Desconocido')
    desc = asset.get('description', '')

    # Mapas simples para estimar riesgo por tipo
    tipo_riesgo = {
        'Base de Datos': 'Alta',
        'Aplicación': 'Alta',
        'Seguridad': 'Media',
        'Infraestructura': 'Media',
        'Información': 'Alta',
        'Almacenamiento': 'Media',
        'Red': 'Media',
        'Documentación': 'Baja'
    }
    riesgo = tipo_riesgo.get(typ, 'Media')

    # Condición (heurística)
    condicion = f"Activo: {name}. Tipo: {typ}. Descripción: {desc or 'Sin descripción adicional.'}"
    if 'backup' in name.lower() or 'backup' in desc.lower() or 'respald' in desc.lower():
        condicion += " | Observación: existen procesos de backup, pero no se encontró verificación automatizada de integridad."
    if 'firewall' in name.lower() or 'cortafuego' in name.lower():
        condicion += " | Observación: cortafuegos presente; se sugiere revisión de reglas y documentación de cambios."

    # Impacto (texto)
    impacto = ("Impacto potencial: pérdida de confidencialidad, integridad y/o disponibilidad. "
               "Podría causar interrupciones en servicios bancarios, pérdidas económicas y sanciones regulatorias.")

    # Mapeo de controles ISO 27001 por tipo
    iso_map = {
        'Base de Datos': ['A.8 Gestión de activos', 'A.10 Criptografía', 'A.12 Operaciones'],
        'Aplicación': ['A.14 Seguridad en desarrollo', 'A.9 Control de acceso', 'A.12 Operaciones'],
        'Seguridad': ['A.11 Control físico', 'A.13 Comunicaciones seguras'],
        'Infraestructura': ['A.12 Operaciones', 'A.13 Gestión de redes'],
        'Información': ['A.8 Gestión de activos', 'A.18 Cumplimiento']
    }
    controles = iso_map.get(typ, ['A.6 Organización de la seguridad'])

    # Recomendación (plantilla)
    recomendacion = (
        f"Se recomienda: 1) Implementar control de acceso con autenticación multifactor y gestión de privilegios; "
        f"2) Cifrado en tránsito y en reposo si aplica; 3) Políticas de backup y pruebas periódicas; "
        f"4) Registro y monitoreo (logs) con retención y protección; 5) Documentar procedimientos y revisiones. "
        f"Alinear acciones con controles ISO-27001: {', '.join(controles)}."
    )

    evidencia = (f"Análisis generado automáticamente (IA local - plantilla). Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC. "
                f"Entrada: nombre={name}, tipo={typ}")

    return {
        "evidencia": evidencia,
        "condicion": condicion,
        "recomendacion": recomendacion,
        "riesgo": riesgo,
        "impacto": impacto,
        "controles_iso": controles
    }

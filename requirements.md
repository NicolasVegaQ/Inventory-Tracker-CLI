📦 Inventory Tracker CLI – Proyecto de Línea de Comandos con Persistencia


## 🧠 Descripción General
    Inventory Tracker CLI es una aplicación de línea de comandos construida con Python puro que permite a los usuarios gestionar el inventario de productos de manera local. A través de una interfaz simple basada en comandos, el usuario puede agregar, actualizar, eliminar, listar productos, cambiar su estado, generar reportes, gestionar categorías y más.

    Este proyecto combina manipulación de archivos, estructuras de datos, control de errores, y diseño de CLI usando argparse. Es ideal para practicar conceptos esenciales como persistencia con JSON, validación de entrada, y modelado de datos.


## 🎯 Objetivo del Proyecto
    Desarrollar un sistema que permita:

    Controlar productos en inventario con propiedades clave

    Almacenar datos en archivos JSON persistentes

    Interactuar a través de comandos en consola

    Implementar funciones adicionales como reportes, historial de cambios y manejo por usuario


## ✅ Funcionalidades Requeridas
    📋 Operaciones básicas
    Agregar productos con nombre, cantidad y categoría

    Actualizar nombre, cantidad o precio por unidad de un producto por ID

    Eliminar productos por ID

    Listar productos por estado, categoría o usuario

    Cambiar el estado de un producto (in-stock, out-of-stock, reserved)

    📊 Reportes
    Ver cantidad total de productos

    Valor total del inventario

    Reporte por categoría

    ⚠️ Alertas
    Mostrar productos con bajo stock (cantidad menor a un umbral configurable)

    🔄 Historial de cambios
    Registrar automáticamente las acciones de actualización y eliminación

    Guardar en un archivo separado inventory_history.json con:

    Timestamp

    Usuario

    Tipo de acción (update, delete)

    Cambios realizados

    👥 Soporte multiusuario (simple)
    Permite asociar cada acción a un usuario con --user

    Permite listar inventario o historial filtrado por usuario

    📁 Importar y exportar
    Importar inventario desde un archivo JSON externo

    Exportar inventario actual a un archivo de respaldo


## Etructura del producto
    {
    "id": "1",
    "name": "Batería AA",
    "quantity": 20,
    "category": "electrónica",
    "status": "in-stock",
    "unit_price": 2500,
    "created_by": "admin",
    "createdAt": "2025-04-14T12:00:00",
    "updatedAt": "2025-04-14T12:00:00"
    }


## 💾 Almacenamiento
    El archivo principal es ~/inventory.json

    El historial de acciones se guarda en ~/inventory_history.json

    Ambos archivos se crean automáticamente si no existen

    Toda la persistencia se maneja con módulos nativos de Python (json, os)


## 🧪 Comandos esperados
    inventory add "Cables USB" 100 --category electronica --price 1500 --user admin
    inventory update 2 --name "Batería 9V" --quantity 15
    inventory delete 4
    inventory list --status in-stock --category electronica
    inventory mark 2 out-of-stock
    inventory report
    inventory import --file productos.json
    inventory export --file backup.json
    inventory history --user admin
    inventory low-stock --threshold 5
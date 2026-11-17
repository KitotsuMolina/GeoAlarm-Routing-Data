# GeoAlarm Libre 0.3.1 para Android

**[Descargar APK firmada](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/geoalarm-libre-v0.3.1/GeoAlarm-Libre-0.3.1.apk)** · 88.0 MiB · Android 8.0 o posterior.

Versión preliminar universal: ARM de 32 y 64 bits, x86 y x86_64.
Paquete Android: `com.kitotsu.geoalarm.libre` · versión de compilación 7.

## Instalación

1. Descargar `GeoAlarm-Libre-0.3.1.apk` desde el enlace anterior.
2. Abrir el archivo en Android y autorizar la instalación desde el navegador o gestor de archivos si Android lo solicita.
3. Revisar los términos y la política de privacidad en la aplicación.
4. Configurar ubicación precisa, ubicación en segundo plano y notificaciones para activar la vigilancia.
5. Para los recorridos, [descargar el ZIP de una región](../../routing-data/spain/README.md) e importarlo desde Ajustes → Datos y privacidad → Rutas en el dispositivo.

Las actualizaciones se instalan sobre la versión anterior usando la misma firma y conservan los datos de la app. La APK no incluye los paquetes regionales.

## Funciones

- Alarmas por entrada y salida de zonas, sonido o vibración y cooldown configurable.
- Marcadores y grupos, historial y copias de datos.
- Ajustes de apariencia, idioma, sonidos y seguimiento del mapa.
- Recorridos y recálculos manuales calculados en el teléfono mediante Valhalla.
- Aportaciones voluntarias mediante Stripe.

El mapa visual utiliza Internet y solo hay una región de rutas activa por instalación. La versión preliminar sigue pendiente de pruebas físicas prolongadas de recorridos y batería.

## Verificación

SHA-256 de la APK:

```text
bc95359a15dd4088a3ae28ff10515426e987b9676c2fc3e0ff29e8eb1da702e9
```

[SHA256SUMS](SHA256SUMS) · [Ficha técnica de la versión](release.json).
La huella pública del certificado de firma está en la ficha; la clave privada permanece fuera del repositorio.

Este repositorio distribuye la APK y los datos de rutas. El código y el historial de la aplicación permanecen en su repositorio privado.

from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_riesgo(humedad, temperatura, lluvia, cultivo=""):

    riesgo = 0

    # HUMEDAD DEL SUELO
    if humedad > 80:
        riesgo += 35
    elif humedad > 60:
        riesgo += 25
    elif humedad > 40:
        riesgo += 10

    # TEMPERATURA
    if temperatura >= 35:
        riesgo += 30
    elif temperatura >= 30:
        riesgo += 20
    elif temperatura >= 25:
        riesgo += 10

    # PROBABILIDAD DE LLUVIA
    if lluvia >= 80:
        riesgo += 35
    elif lluvia >= 50:
        riesgo += 25
    elif lluvia >= 30:
        riesgo += 10

    # AJUSTE SEGÚN EL CULTIVO
    if cultivo.lower() == "arroz":
        if humedad < 40:
            riesgo += 10

    elif cultivo.lower() == "maiz":
        if humedad < 35:
            riesgo += 10

    elif cultivo.lower() == "papa":
        if humedad > 80:
            riesgo += 10

    # LÍMITE MÁXIMO
    if riesgo > 100:
        riesgo = 100

    # NIVEL DE RIESGO
    if riesgo <= 30:
        nivel = "Bajo"
        color = "🟢"

    elif riesgo <= 60:
        nivel = "Precaución"
        color = "🟡"

    elif riesgo <= 80:
        nivel = "Alto"
        color = "🟠"

    else:
        nivel = "Emergencia"
        color = "🔴"

         # RECOMENDACIONES INTELIGENTES

    if humedad > 80 and lluvia >= 50:

        recomendacion = (
            "🚨 NO RIEGUES HOY. "
            "El suelo presenta mucha humedad y existe "
            "una elevada probabilidad de lluvia. "
            "Revisa los drenajes."
        )

    elif temperatura >= 35:

        recomendacion = (
            "🌡️ VIGILAR TEMPERATURA. "
            "La temperatura es elevada. "
            "Monitorea el estado del cultivo y la humedad del suelo."
        )

    elif humedad < 40:

        recomendacion = (
            "💧 REVISAR RIEGO. "
            "El suelo presenta poca humedad. "
            "Evalúa si el cultivo necesita riego."
        )

    elif lluvia >= 80:

        recomendacion = (
            "🌧️ PREPARAR LA PARCELA. "
            "Existe una alta probabilidad de lluvia. "
            "Revisa los drenajes y evita riegos innecesarios."
        )

    elif riesgo >= 61:

        recomendacion = (
            "⚠️ RIESGO ELEVADO. "
            "Revisa las condiciones de la parcela antes "
            "de realizar actividades agrícolas."
        )

    elif riesgo >= 31:

        recomendacion = (
            "🟡 MONITOREAR LA PARCELA. "
            "Se presentan algunas condiciones que podrían generar "
            "riesgo. Mantén vigilancia sobre la humedad, temperatura "
            "y probabilidad de lluvia."
        )

    else:

        recomendacion = (
            "✅ CONDICIONES FAVORABLES. "
            "Continúa monitoreando tu parcela."
        )

    return riesgo, nivel, color, recomendacion


@app.route("/")
def inicio():

    humedad = 78
    temperatura = 31
    lluvia = 60

    riesgo, nivel, color, recomendacion = calcular_riesgo(
        humedad,
        temperatura,
        lluvia
    )

    return render_template(
        "index.html",
        humedad=humedad,
        temperatura=temperatura,
        lluvia=lluvia,
        riesgo=riesgo,
        nivel=nivel,
        color=color,
        recomendacion=recomendacion
    )


@app.route("/analizar", methods=["POST"])
def analizar():

    humedad = float(request.form.get("humedad", 0))
    temperatura = float(request.form.get("temperatura", 0))
    lluvia = float(request.form.get("lluvia", 0))

    nombre_parcela = request.form.get("nombre_parcela", "")
    cultivo = request.form.get("cultivo", "")

    riesgo, nivel, color, recomendacion = calcular_riesgo(
        humedad,
        temperatura,
        lluvia,
        cultivo
    )

    return render_template(
        "index.html",
        nombre_parcela=nombre_parcela,
        cultivo=cultivo,
        humedad=humedad,
        temperatura=temperatura,
        lluvia=lluvia,
        riesgo=riesgo,
        nivel=nivel,
        color=color,
        recomendacion=recomendacion
    )


@app.route("/registrar", methods=["POST"])
def registrar():

    nombre_parcela = request.form.get("nombre_parcela", "")
    ubicacion = request.form.get("ubicacion", "")
    cultivo = request.form.get("cultivo", "")
    area = request.form.get("area", "")
    fecha_siembra = request.form.get("fecha_siembra", "")
    riego = request.form.get("riego", "")

    # Datos de ejemplo para la demostración
    humedad = 35
    temperatura = 31
    lluvia = 60

    riesgo, nivel, color, recomendacion = calcular_riesgo(
        humedad,
        temperatura,
        lluvia,
        cultivo
    )

    return render_template(
        "index.html",
        nombre_parcela=nombre_parcela,
        ubicacion=ubicacion,
        cultivo=cultivo,
        area=area,
        fecha_siembra=fecha_siembra,
        riego=riego,
        parcela_registrada=True,
        humedad=humedad,
        temperatura=temperatura,
        lluvia=lluvia,
        riesgo=riesgo,
        nivel=nivel,
        color=color,
        recomendacion=recomendacion
    )


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, flash, redirect, render_template, request, url_for

from config.database import initialize_database
from modules.catalogos.service import CatalogoService
from modules.tickets.service import ESTADOS_PERMITIDOS, TicketService
from modules.usuarios.service import UsuarioService

app = Flask(__name__)
app.secret_key = "mesa-ayuda-demo-semana13"

catalogos = CatalogoService()
usuarios = UsuarioService()
tickets = TicketService()


def preparar_datos_demo():
    initialize_database()
    semillas_catalogos = [
        ("categoria", "Hardware", "Fallas fisicas en equipos"),
        ("categoria", "Software", "Problemas con programas o sistema operativo"),
        ("prioridad", "Alta", "Atencion inmediata"),
        ("prioridad", "Media", "Atencion normal"),
        ("prioridad", "Baja", "Puede atenderse despues"),
    ]
    for tipo, nombre, descripcion in semillas_catalogos:
        try:
            catalogos.crear(tipo, nombre, descripcion)
        except ValueError:
            pass
    try:
        usuarios.crear(
            "Ana Solicitante",
            "ana.solicitante@empresa.com",
            "asolicitante",
            "solicitante",
        )
    except ValueError:
        pass


@app.context_processor
def inject_globals():
    return {"estados": sorted(ESTADOS_PERMITIDOS)}


@app.route("/")
def dashboard():
    lista_catalogos = catalogos.listar()
    lista_usuarios = usuarios.listar()
    lista_tickets = tickets.listar()
    abiertos = [t for t in lista_tickets if t["estado"] not in {"Resuelto", "Cerrado"}]
    return render_template(
        "dashboard.html",
        total_catalogos=len(lista_catalogos),
        total_usuarios=len(lista_usuarios),
        total_tickets=len(lista_tickets),
        tickets_abiertos=len(abiertos),
        tickets_recientes=lista_tickets[:5],
    )


@app.route("/tickets", methods=["GET", "POST"])
def vista_tickets():
    if request.method == "POST":
        try:
            tickets.crear(
                request.form.get("solicitante_id"),
                request.form.get("categoria_id"),
                request.form.get("prioridad_id"),
                request.form.get("descripcion"),
            )
            flash("Ticket creado correctamente.", "success")
            return redirect(url_for("vista_tickets"))
        except ValueError as error:
            flash(str(error), "error")

    return render_template(
        "tickets.html",
        tickets=tickets.listar(),
        usuarios=usuarios.listar(),
        categorias=catalogos.listar("categoria"),
        prioridades=catalogos.listar("prioridad"),
    )


@app.route("/tickets/<folio>")
def detalle_ticket(folio):
    ticket = tickets.obtener_por_folio(folio)
    if not ticket:
        flash("Ticket no encontrado.", "error")
        return redirect(url_for("vista_tickets"))
    return render_template(
        "ticket_detalle.html",
        ticket=ticket,
        categorias=catalogos.listar("categoria"),
        prioridades=catalogos.listar("prioridad"),
    )


@app.route("/tickets/<folio>/actualizar", methods=["POST"])
def actualizar_ticket(folio):
    try:
        tickets.actualizar(
            folio,
            request.form.get("categoria_id"),
            request.form.get("prioridad_id"),
            request.form.get("descripcion"),
            request.form.get("estado"),
        )
        flash("Ticket actualizado correctamente.", "success")
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("detalle_ticket", folio=folio))


@app.route("/tickets/<folio>/eliminar", methods=["POST"])
def eliminar_ticket(folio):
    try:
        tickets.eliminar(folio)
        flash("Ticket eliminado correctamente.", "success")
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("vista_tickets"))


@app.route("/usuarios", methods=["GET", "POST"])
def vista_usuarios():
    if request.method == "POST":
        try:
            usuarios.crear(
                request.form.get("nombre"),
                request.form.get("correo"),
                request.form.get("usuario"),
                request.form.get("rol"),
            )
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("vista_usuarios"))
        except ValueError as error:
            flash(str(error), "error")
    return render_template("usuarios.html", usuarios=usuarios.listar())


@app.route("/catalogos", methods=["GET", "POST"])
def vista_catalogos():
    if request.method == "POST":
        try:
            catalogos.crear(
                request.form.get("tipo"),
                request.form.get("nombre"),
                request.form.get("descripcion"),
            )
            flash("Catalogo creado correctamente.", "success")
            return redirect(url_for("vista_catalogos"))
        except ValueError as error:
            flash(str(error), "error")
    return render_template("catalogos.html", catalogos=catalogos.listar())


if __name__ == "__main__":
    preparar_datos_demo()
    app.run(debug=True)

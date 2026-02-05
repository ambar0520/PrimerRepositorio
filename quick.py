import uuid
from datetime import datetime

# -------------------------------
# Clase Pedido
# -------------------------------
class Pedido:
    def __init__(self, order_id, nombre, apellido, cajas):
        self.order_id = order_id
        self.nombre = nombre
        self.apellido = apellido
        self.cajas = cajas
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = "PENDIENTE"

    def __str__(self):
        return f"[{self.order_id}] {self.nombre} {self.apellido} - Cajas:{self.cajas} - {self.fecha} - Estado:{self.estado}"

# -------------------------------
# Clase Incidencia
# -------------------------------
class Incidencia:
    def __init__(self, incident_id, tipo, order_id, motivo):
        self.incident_id = incident_id
        self.tipo = tipo
        self.order_id = order_id
        self.motivo = motivo
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = "PENDIENTE"

    def __str__(self):
        return f"[{self.incident_id}] Tipo:{self.tipo} - Pedido:{self.order_id} - Motivo:{self.motivo} - {self.fecha} - Estado:{self.estado}"

# -------------------------------
# Nodo genérico
# -------------------------------
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

# -------------------------------
# Cola de pedidos (FIFO)
# -------------------------------
class ColaPedidos:
    def __init__(self):
        self.frente = None
        self.final = None

    def esta_vacia(self):
        return self.frente is None

    def enqueue(self, pedido):
        nuevo = Nodo(pedido)
        if self.esta_vacia():
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def dequeue(self):
        if self.esta_vacia():
            return None
        pedido = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        return pedido

    def peek(self):
        return None if self.esta_vacia() else self.frente.dato

    def mostrar(self):
        actual = self.frente
        lista = []
        while actual:
            lista.append(str(actual.dato))
            actual = actual.siguiente
        return lista

# -------------------------------
# Pila de incidencias (LIFO)
# -------------------------------
class PilaIncidencias:
    def __init__(self):
        self.tope = None

    def esta_vacia(self):
        return self.tope is None

    def push(self, incidencia):
        nuevo = Nodo(incidencia)
        nuevo.siguiente = self.tope
        self.tope = nuevo

    def pop(self):
        if self.esta_vacia():
            return None
        incidencia = self.tope.dato
        self.tope = self.tope.siguiente
        return incidencia

    def peek(self):
        return None if self.esta_vacia() else self.tope.dato

    def mostrar(self):
        actual = self.tope
        lista = []
        while actual:
            lista.append(str(actual.dato))
            actual = actual.siguiente
        return lista

# -------------------------------
# Aplicación principal
# -------------------------------
class QuickDispatchApp:
    def __init__(self):
        self.pedidos = ColaPedidos()
        self.despachados = {}
        self.incidencias = PilaIncidencias()
        self.procesadas = {}
        self.last_dispatched = None
        self.last_processed = None
        self.order_counter = 1

    def generar_order_id(self):
        oid = f"Order-{self.order_counter:04d}"
        self.order_counter += 1
        return oid

    def generar_incident_id(self):
        return str(uuid.uuid4())[:8]

    def registrar_pedido(self):
        nombre = input("Nombre del cliente: ").strip()
        apellido = input("Apellido del cliente: ").strip()
        cajas = input("Cantidad de cajas: ").strip()

        if not nombre or not apellido or not cajas.isdigit() or int(cajas) <= 0:
            print("⚠️ Datos inválidos.")
            return

        order_id = self.generar_order_id()
        pedido = Pedido(order_id, nombre, apellido, int(cajas))
        self.pedidos.enqueue(pedido)
        print(f"✅ Pedido registrado: {pedido}")

    def despachar_pedido(self):
        pedido = self.pedidos.dequeue()
        if not pedido:
            print("⚠️ No hay pedidos pendientes.")
            return
        pedido.estado = "DESPACHADO"
        self.despachados[pedido.order_id] = pedido
        self.last_dispatched = pedido.order_id
        print(f"🚚 Pedido despachado: {pedido}")

    def registrar_incidencia(self):
        tipo = input("Tipo (DEVOLUCIÓN/CANCELACIÓN): ").strip().upper()
        order_id = input("Order ID: ").strip()
        motivo = input("Motivo: ").strip()

        if tipo not in ["DEVOLUCIÓN", "CANCELACIÓN"] or not motivo:
            print("⚠️ Datos inválidos.")
            return
        if order_id not in self.despachados:
            print("⚠️ Pedido no existe o no está despachado.")
            return

        pedido = self.despachados[order_id]
        if pedido.estado == "CERRADO":
            print("⚠️ Pedido ya cerrado.")
            return

        incident_id = self.generar_incident_id()
        incidencia = Incidencia(incident_id, tipo, order_id, motivo)
        self.incidencias.push(incidencia)
        pedido.estado = "DEVUELTO" if tipo == "DEVOLUCIÓN" else "CANCELADO"
        print(f"🔄 Incidencia registrada: {incidencia}")

    def procesar_incidencia(self):
        incidencia = self.incidencias.pop()
        if not incidencia:
            print("⚠️ No hay incidencias pendientes.")
            return
        incidencia.estado = "PROCESADA"
        self.procesadas[incidencia.incident_id] = incidencia
        self.last_processed = incidencia.incident_id
        pedido = self.despachados[incidencia.order_id]
        pedido.estado = "CERRADO"
        print(f"✅ Incidencia procesada: {incidencia}")
        print(f"📦 Pedido cerrado: {pedido}")

    def ver_estado(self):
        print("\n--- ESTADO DEL SISTEMA ---")
        print("📦 Pendientes:", len(self.pedidos.mostrar()))
        print("\n".join(self.pedidos.mostrar()) or "No hay pedidos pendientes")
        print("\n🚚 Despachados:", len(self.despachados))
        for p in self.despachados.values():
            print(p)
        print(f"Último despachado: {self.last_dispatched}")
        print("\n🔄 Incidencias pendientes:", len(self.incidencias.mostrar()))
        print("\n".join(self.incidencias.mostrar()) or "No hay incidencias pendientes")
        print("\n✅ Incidencias procesadas:", len(self.procesadas))
        for i in self.procesadas.values():
            print(i)
        print(f"Última procesada: {self.last_processed}")

    def salir(self):
        print("\n--- RESUMEN FINAL ---")
        print("📦 Pendientes:", len(self.pedidos.mostrar()))
        print("🚚 Despachados:", len(self.despachados))
        print("🔄 Incidencias pendientes:", len(self.incidencias.mostrar()))
        print("✅ Incidencias procesadas:", len(self.procesadas))
        print("👋 Saliendo del sistema...")

    def menu(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Registrar pedido")
            print("2. Despachar pedido")
            print("3. Registrar devolución/cancelación")
            print("4. Procesar devolución/cancelación")
            print("5. Ver estado")
            print("6. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_pedido()
            elif opcion == "2":
                self.despachar_pedido()
            elif opcion == "3":
                self.registrar_incidencia()
            elif opcion == "4":
                self.procesar_incidencia()
            elif opcion == "5":
                self.ver_estado()
            elif opcion == "6":
                self.salir()
                break
if __name__ == "__main__":
    app = QuickDispatchApp()
    app.menu()
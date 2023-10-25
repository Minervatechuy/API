from app import db, ma
import bcrypt

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class CalculadorasPresupuestosClientes(db.Model):
    __tablename__ = 'calculadoras_presupuestos_clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255))
    presupuestos_id = db.Column(db.Integer)
    fecha = db.Column(db.Date, nullable=True)
    email_cliente = db.Column(db.String(510), nullable=True)

class Calculators(db.Model):
    __tablename__ = 'calculators'
    token = db.Column(db.String(40), primary_key=True)
    url = db.Column(db.String(255), nullable=True)
    ip = db.Column(db.String(255), nullable=True)
    formula = db.Column(db.String(5100), nullable=True)
    entity_ID = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    activo = db.Column(db.Boolean, nullable=True)

class Clientes(db.Model):
    __tablename__ = 'clientes'
    email = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(255), nullable=False)

class EntidadesCalculadoras(db.Model):
    __tablename__ = 'entidades_calculadoras'
    id_entidad = db.Column(db.String(255), primary_key=True)
    token = db.Column(db.String(255), primary_key=True)

class Entities(db.Model):
    __tablename__ = 'entities'
    ID = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(250), nullable=True)
    type = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, nullable=False)
    descripcion = db.Column(db.String(1024), nullable=False)

class Etapa(db.Model):
    __tablename__ = 'etapa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    subtitulo = db.Column(db.String(255), nullable=False)
    posicion = db.Column(db.Integer, nullable=False)

class EtapaData(db.Model):
    __tablename__ = 'etapa_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    etapa_id = db.Column(db.Integer, nullable=False)
    meta_key = db.Column(db.String(2550), nullable=False)
    meta_value = db.Column(db.String(2550), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

class EtapaOpcion(db.Model):
    __tablename__ = 'etapa_opcion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    etapa_id = db.Column(db.Integer, nullable=False)
    meta_key = db.Column(db.String(2550), nullable=False)
    meta_value = db.Column(db.String(2550), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

class Logs(db.Model):
    __tablename__ = 'logs'
    date = db.Column(db.String(10), primary_key=True)
    time = db.Column(db.String(8), primary_key=True)
    procedure = db.Column(db.String(100), primary_key=True)
    _in = db.Column(db.String(250), primary_key=True)
    _out = db.Column(db.String(250), primary_key=True)

class Presupuestos(db.Model):
    __tablename__ = 'presupuestos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resultado = db.Column(db.Integer, nullable=True)
    formula = db.Column(db.String(2550), nullable=True)
    finalizado = db.Column(db.Boolean, nullable=True)

class PresupuestosData(db.Model):
    __tablename__ = 'presupuestos_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    presupuesto_id = db.Column(db.Integer, nullable=False)
    meta_key = db.Column(db.String(2550), nullable=False)
    meta_value = db.Column(db.String(2550), nullable=False)
    etapa_id = db.Column(db.Integer, nullable=False)

class Tokens(db.Model):
    __tablename__ = 'tokens'
    token = db.Column(db.String(255), primary_key=True)
    vendido = db.Column(db.Boolean, nullable=False)
    canjeado = db.Column(db.Boolean, nullable=False)
    fechaFin = db.Column(db.Date, nullable=False)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    mail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(14), nullable=True)
    nombre = db.Column(db.String(255), nullable=False)
    ultimoAcceso = db.Column(db.Date, nullable=False)
    ultimaIP = db.Column(db.String(15), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, mail, password, telefono, nombre, ultimoAcceso, ultimaIP, apellidos, activo, imagen):
        self.mail = mail
        self.password = self.set_password(password)
        self.telefono = telefono
        self.nombre = nombre
        self.ultimoAcceso = ultimoAcceso
        self.ultimaIP = ultimaIP
        self.apellidos = apellidos
        self.activo = activo
        self.imagen = imagen

    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

class UsersToCalculators(db.Model):
    __tablename__ = 'users_to_calculators'
    user_email = db.Column(db.String(255), db.ForeignKey('usuarios.mail'), primary_key=True)
    calculator_token = db.Column(db.String(40), db.ForeignKey('calculators.token'), primary_key=True)

class UsersToEntities(db.Model):
    __tablename__ = 'users_to_entites'
    user_email = db.Column(db.String(255), db.ForeignKey('usuarios.mail'), primary_key=True)
    entity_id = db.Column(db.String(50), db.ForeignKey('entities.ID'), primary_key=True)
    
class CalculadorasPresupuestosClientesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CalculadorasPresupuestosClientes

class CalculatorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Calculators

class ClientesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Clientes

class EntidadesCalculadorasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntidadesCalculadoras

class EntitiesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entities

class EtapaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Etapa

class EtapaDataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EtapaData

class EtapaOpcionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EtapaOpcion

class LogsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Logs

class PresupuestosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Presupuestos

class PresupuestosDataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PresupuestosData

class TokensSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tokens

class UsersToCalculatorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsersToCalculators

class UsersToEntitiesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsersToEntities

class UsuariosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios

    # Agregar un campo para la columna 'imagen'
    imagen = fields.Field(data_key='imagen', serialize='bytes')

    # Resto de los campos
    mail = ma.auto_field()
    password = ma.auto_field()
    telefono = ma.auto_field()
    nombre = ma.auto_field()
    ultimoAcceso = ma.auto_field()
    ultimaIP = ma.auto_field()
    apellidos = ma.auto_field()
    activo = ma.auto_field()


calculadoras_presupuestos_clientes_schema = CalculadorasPresupuestosClientesSchema()
calculators_schema = CalculatorsSchema()
clientes_schema = ClientesSchema()
entidades_calculadoras_schema = EntidadesCalculadorasSchema()
entities_schema = EntitiesSchema()
etapa_schema = EtapaSchema()
etapa_data_schema = EtapaDataSchema()
etapa_opcion_schema = EtapaOpcionSchema()
logs_schema = LogsSchema()
presupuestos_schema = PresupuestosSchema()
presupuestos_data_schema = PresupuestosDataSchema()
tokens_schema = TokensSchema()
users_to_calculators_schema = UsersToCalculatorsSchema()
users_to_entities_schema = UsersToEntitiesSchema()
usuarios_schema = UsuariosSchema()


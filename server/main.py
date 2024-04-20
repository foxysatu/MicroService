from flask import Flask, render_template, redirect, request, session
from keycloak import KeycloakOpenID
from prometheus_flask_exporter import PrometheusMetrics
import os

# Импорт необходимых модулей Flask для создания веб-приложения
# и работы с Keycloak для аутентификации пользователей,
# а также для мониторинга приложения с помощью Prometheus

# Инициализация приложения Flask
app = Flask(__name__)
# Устанавливаем отладочный режим Flask в False (по умолчанию)
app.debug = False

# Устанавливаем секретный ключ для подписи сессий,
# который используется для безопасного хранения данных сессии
app.secret_key = "SOMTHING_UNIQUE_AND_SECRET"

# Инициализация клиента KeycloakOpenID для взаимодействия с Keycloak
keycloak_openid = KeycloakOpenID(
    # URL-адрес сервера Keycloak, который берется из переменной окружения,
    # если она существует, иначе используется значение по умолчанию
    server_url=os.getenv("KEYCLOAK_URL", "http://keycloakapp:8080/"),
    # Идентификатор клиента в Keycloak
    client_id="ivan-client",
    # Название области в Keycloak
    realm_name="ivan",
    # Секретный ключ клиента для аутентификации
    client_secret_key="e83WqUJSxI9KGU79FRNwlSsYpFaiaL73",
)

# Инициализация PrometheusMetrics для мониторинга приложения
metrics = PrometheusMetrics(app)

# Функция для проверки наличия JWT-токена в заголовке запроса
def check_header():
    # Получаем токен из заголовка запроса
    token = request.headers.get('JWT-TOKEN')
    if token:
        # Интроспектируем токен для получения информации о нем
        token_info = keycloak_openid.introspect(token["access_token"])
        print(token_info)
        # Журналируем роли пользователя
        app.logger.info(f"Роли пользователя: {token_info['realm_access']['roles']}")
        if "movie" not in token_info["realm_access"]["roles"]:
            # Если у пользователя нет необходимой роли, отображаем страницу входа с соответствующим сообщением
            return render_template(
                "login.html",
                wrong_datg_visability="collapse",
                no_permission_visability="visible",
            )
        else:
            # Если у пользователя есть необходимая роль, устанавливаем сессию как действительную и отображаем главную страницу
            session["valid"] = True
            return render_template("index.html")

# Маршрут для главной страницы
@app.route('/', methods=["POST", "GET"])
def index():
    # Проверяем, действительна ли сессия пользователя
    if session.get("valid", False):
        # Если сессия действительна, отображаем главную страницу
        return render_template('index.html')
    # Если метод запроса POST, это означает, что пользователь отправил форму входа
    if request.method == "POST":
        # Получаем данные из формы
        print(request.form)
        username = str(request.form["fname"])
        password = str(request.form["lname"])
        # Пытаемся получить токен от Keycloak с помощью предоставленных учетных данных
        try:
            token = keycloak_openid.token(username, password)
            # Получаем информацию о пользователе из полученного токена
            userinfo = keycloak_openid.userinfo(token["access_token"])
            app.logger.info(f"Информация о пользователе: {userinfo}")
            # Интроспектируем полученный токен для получения информации о нем
            token_info = keycloak_openid.introspect(token["access_token"])
            print(token_info)
            app.logger.info(f"Роли пользователя: {token_info['realm_access']['roles']}")
            # Проверяем, имеет ли пользователь необходимую роль "movie"
            if "movie" not in token_info["realm_access"]["roles"]:
                # Если у пользователя нет необходимой роли, отображаем страницу входа с сообщением о недостаточных правах
                return render_template(
                    "login.html",
                    wrong_datg_visability="collapse",
                    no_permission_visability="visible",
                )
            else:
                # Если у пользователя есть необходимая роль, устанавливаем сессию как действительную и отображаем главную страницу
                session["valid"] = True
                return render_template("index.html")
        # Если произошла ошибка при получении токена (например, неправильные учетные данные), логируем ее и отображаем страницу входа с сообщением об ошибке
        except Exception as e:
            app.logger.error(e)
            return render_template(
                "login.html",
                wrong_datg_visability="visible",
                no_permission_visability="collapse",
            )

    # Если метод запроса GET и сессия не действительна, отображаем страницу входа с сообщением об отсутствии ошибок
    return render_template(
        "login.html",
        wrong_datg_visability="collapse",
        no_permission_visability="collapse",
    )

# Маршрут для получения всех данных
@app.route('/all')
def fetch_all():
    return render_template('all.html')

# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    # Помечаем сессию пользователя как недействительную и перенаправляем на главную страницу
    session["valid"] = False
    return redirect("/")

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051)

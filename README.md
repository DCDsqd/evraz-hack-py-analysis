# Анализ проекта `evraz-hack`

Этот документ представляет собой отчет о текущем состоянии проекта, выполненный на **30.11.2024**. В нем содержится информация о нарушениях архитектуры, несоответствиях стандартам кодирования и других ошибках, обнаруженных в проекте.

---

## Дата последнего изменения

- **Дата анализа**: 29.11.2024
- **Дата последнего изменения проекта**: 30.11.2024

---

## Общее количество ошибок

- **Общее количество ошибок**: 3
- **Архитектурных нарушений**: 1
- **Несоответствий стандартам**: 1

---

## Детальный анализ ошибок

### 1. Архитектурное нарушение

#### Проблема:

В файле `chat_service.py` используются прямые обращения к модели данных, что нарушает принципы чистой архитектуры. Логика работы с базой данных должна быть вынесена в отдельный слой репозиториев, а сервисы должны работать через интерфейсы.

#### Пример нарушения:

```python
user = User.query.filter_by(username=token).first()
location = Location.query.filter_by(name=name).first()
Предложенное исправление:
Необходимо создать репозиторий, который будет отвечать за работу с моделями User и Location, и использовать его в сервисе. Например:

class UserRepository:
    def get_by_username(self, username: str) -> User:
        return User.query.filter_by(username=username).first()

class LocationRepository:
    def get_by_name(self, name: str) -> Location:
        return Location.query.filter_by(name=name).first()
Затем в chat_service.py сервис должен использовать эти репозитории:

class ChatService:
    def __init__(self, user_repo: UserRepository, location_repo: LocationRepository):
        self.user_repo = user_repo
        self.location_repo = location_repo

    def get_user_location(self, token: str, name: str):
        user = self.user_repo.get_by_username(token)
        location = self.location_repo.get_by_name(name)
        return user, location
2. Нарушение стиля кода
Проблема:
В файле LinkFragmentValidator.cs используется условный оператор без фигурных скобок, что нарушает стандарты стиля кодирования.

Пример нарушения:
if (!Guid.TryParse(fragment.Target, out Guid dealerId))
    return ValidationResult.Error("Target must be of typ Guid");
Предложенное исправление:
Добавить фигурные скобки для улучшения читаемости и предотвращения потенциальных ошибок:

if (!Guid.TryParse(fragment.Target, out Guid dealerId)) {
    return ValidationResult.Error("Target must be of typ Guid");
}
3. Некорректное наименование типа
Проблема:
В файле ui.tsx используется тип ProductProps, который не соответствует наименованию компонента ProductItem.

Пример нарушения:
type ProductProps = {
  product: Product;
  theme: Theme;
  setProduct: (product: Product) => void;
};
Предложенное исправление:
Переименовать тип в ProductItemProps, чтобы он отражал наименование компонента:

type ProductItemProps = {
  product: Product;
  theme: Theme;
  setProduct: (product: Product) => void;
};
Как исправить ошибки
Архитектурное нарушение:

Выносите логику работы с моделями в репозитории, следуя принципам чистой архитектуры.
Создайте интерфейсы для репозиториев и используйте их в сервисах.
Нарушение стиля кода:

Добавьте фигурные скобки для улучшения читаемости и безопасности кода, даже если условие однонаправленное.
Некорректное наименование типа:

Переименуйте тип, чтобы он соответствовал компоненту и лучше описывал его назначение.
Стандарты кодирования
В проекте применяются следующие стандарты кодирования:

Pylint для Python-кода
ESLint для TypeScript
RCS для C#
Используйте эти инструменты для автоматической проверки качества кода.

Разработка и контрибьюции
Форк репозитория и клонируйте на свой локальный компьютер:

git clone https://github.com/your_username/project_name.git
Создайте свою ветку:

git checkout -b fix/your-fix-name
Внесите изменения, убедитесь, что исправления соответствуют стандартам и рекомендациям из этого документа.

Создайте пулл-запрос для внесения изменений в основной репозиторий.
Анализ проекта ```project_name``` от 01.01.2024 00:00:00 UTC+3 
---
Дата последнего изменения проекта : 01.01.2024 00:00:00 UTC+3

Общее количество ошибок: 3
Архитектурных нарушений: 1
... _<Перечисление других классов ошибок>_
Несоответствий стандартам: 1 

### Архитектурное нарушение
> `chat_service.py` (номер строки:номер символа, при наличии)
>  Необходимо вынести в слой адаптеров, работать через репозитории и интерфейсы из сервисов

```python
user = User.query.filter_by(username=token).first()
location = Location.query.filter_by(name=name).first()
```

### Краткое описание нарушения (Add braces to if statement)
> `LinkFragmentValidator.cs` (номер строки:номер символа, при наличии)
> `Severity`	`Code`	`Description`	`Project`	`File`	`Line`	
> Error (active)	RCS1007	Add braces to if statement	Eurofurence.App.Server.Services	LinkFragmentValidator.cs    35

```csharp
if (!Guid.TryParse(fragment.Target, out Guid dealerId))
    return ValidationResult.Error("Target must be of typ Guid");
```
> Предложенное исправление

```csharp
if (!Guid.TryParse(fragment.Target, out Guid dealerId)) {
    return ValidationResult.Error("Target must be of typ Guid");
}
```

### Некорректное наименование
> `ui.tsx` (номер строки:номер символа, при наличии)
> Поскольку этот тип относится к компоненту ProductItem и отражает его интерфейс, то тип должен называться ProductItemProps

```ts
type ProductProps = {
  product: Product;
  theme: Theme;
  setProduct: (product: Product) => void;
};
```

> Предложенное исправление

```ts
type ProductItemProps = {
  product: Product;
  theme: Theme;
  setProduct: (product: Product) => void;
};
```
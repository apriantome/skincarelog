# === Stage 5: Связи между сущностями ===
# Project: SkinCareLog
def get_applications(product, applications_by_product):
    """Возвращает список применений для заданного средства.

    applications_by_product: dict, маппинг id средства -> список применений.
    """
    return list(applications_by_product.get(product, []))


def build_applications_index(products, applications):
    """Собирает индекс применений по средствам из исходных данных.

    products: список средств (с полем id).
    applications: список применений, каждое содержит id средства.
    """
    applications_by_product = {}
    for application in applications:
        product_id = application.get("product_id")
        applications_by_product.setdefault(product_id, []).append(application)
    return applications_by_product


def check_integrity(product, applications_by_product):
    """Проверяет целостность связи средство -> применения.

    Возвращает True, если связь непротиворечива, иначе False.
    """
    if product is None:
        return False

    applications = applications_by_product.get(product, [])
    for application in applications:
        product_id = application.get("product_id")
        if product_id != product:
            return False
    return True


def link_applications(products, applications):
    """Привязывает к каждому средству его применения.

    products: список средств (с полем id и полем applications).
    applications: список применений, каждое содержит product_id.
    """
    applications_by_id = {}
    for application in applications:
        product_id = application.get("product_id")
        applications_by_id.setdefault(product_id, []).append(application)

    for product in products:
        product_id = product.get("id")
        product.setdefault("applications", [])
        product["applications"] = applications_by_id.get(product_id, [])

    return products


def find_applications_by_product_id(product_id, applications):
    """Возвращает применения, относящиеся к средству с данным id."""
    return [application for application in applications if application.get("product_id") == product_id]

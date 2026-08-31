from sqlalchemy import select

from app.db.postgres import SessionLocal
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


PERMISSIONS = [
    ("workflow:create", "Create workflows"),
    ("workflow:read", "View workflows"),
    ("workflow:update", "Update workflows"),
    ("workflow:delete", "Delete workflows"),
    ("workflow:execute", "Execute workflows"),
    ("workflow:approve", "Approve workflow steps"),
    ("user:create", "Create users"),
    ("user:read", "View users"),
    ("user:update", "Update users"),
    ("user:delete", "Delete users"),
]


ROLES = {
    "ADMIN": [
        "workflow:create",
        "workflow:read",
        "workflow:update",
        "workflow:delete",
        "workflow:execute",
        "workflow:approve",
        "user:create",
        "user:read",
        "user:update",
        "user:delete",
    ],
    "MANAGER": [
        "user:read",
        "workflow:create",
        "workflow:read",
        "workflow:update",
        "workflow:execute",
        "workflow:approve",
    ],
    "EMPLOYEE": [
        "workflow:read",
        "workflow:execute",
    ],
}


def seed_permissions(db):
    permission_map = {}

    for name, description in PERMISSIONS:
        permission = db.scalar(
            select(Permission).where(
                Permission.name == name
            )
        )

        if not permission:
            permission = Permission(
                name=name,
                description=description,
            )

            db.add(permission)
            db.flush()

        permission_map[name] = permission

    return permission_map


def seed_roles(db):
    role_map = {}

    for role_name in ROLES:
        role = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if not role:
            role = Role(name=role_name)

            db.add(role)
            db.flush()

        role_map[role_name] = role

    return role_map


def seed_role_permissions(
    db,
    role_map,
    permission_map,
):
    for role_name, permission_names in ROLES.items():
        role = role_map[role_name]

        for permission_name in permission_names:
            permission = permission_map[permission_name]

            existing = db.scalar(
                select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
            )

            if not existing:
                db.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )


def seed():
    db = SessionLocal()

    try:
        permission_map = seed_permissions(db)

        role_map = seed_roles(db)

        seed_role_permissions(
            db,
            role_map,
            permission_map,
        )

        db.commit()

        print("RBAC seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
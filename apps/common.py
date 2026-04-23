from apps.auditlogs.models import AuditLog


def create_audit_log(*, user, action, instance, description):
    AuditLog.objects.create(
        user=user if getattr(user, 'is_authenticated', False) else None,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=instance.pk or 0,
        description=description,
    )

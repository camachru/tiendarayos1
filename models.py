# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CartAddress(models.Model):
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1)
    default = models.BooleanField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_address'


class CartCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cart_category'


class CartColourvariation(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cart_colourvariation'


class CartOrder(models.Model):
    start_date = models.DateTimeField()
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField()
    billing_address = models.ForeignKey(CartAddress, models.DO_NOTHING, blank=True, null=True)
    shipping_address = models.ForeignKey(CartAddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart_order'


class CartOrderitem(models.Model):
    quantity = models.IntegerField()
    colour = models.ForeignKey(CartColourvariation, models.DO_NOTHING)
    order = models.ForeignKey(CartOrder, models.DO_NOTHING)
    product = models.ForeignKey('CartProduct', models.DO_NOTHING)
    size = models.ForeignKey('CartSizevariation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_orderitem'


class CartPayment(models.Model):
    payment_method = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    succesful = models.BooleanField()
    amount = models.FloatField()
    raw_response = models.TextField()
    order = models.ForeignKey(CartOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_payment'


class CartProduct(models.Model):
    title = models.CharField(max_length=150)
    slug = models.CharField(unique=True, max_length=50)
    image = models.CharField(max_length=100)
    descritption = models.TextField()
    price = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    active = models.BooleanField()
    primary_category = models.ForeignKey(CartCategory, models.DO_NOTHING)
    stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_product'


class CartProductAvailableColours(models.Model):
    product = models.ForeignKey(CartProduct, models.DO_NOTHING)
    colourvariation = models.ForeignKey(CartColourvariation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_product_available_colours'
        unique_together = (('product', 'colourvariation'),)


class CartProductAvailableSizes(models.Model):
    product = models.ForeignKey(CartProduct, models.DO_NOTHING)
    sizevariation = models.ForeignKey('CartSizevariation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_product_available_sizes'
        unique_together = (('product', 'sizevariation'),)


class CartProductSecondaryCategories(models.Model):
    product = models.ForeignKey(CartProduct, models.DO_NOTHING)
    category = models.ForeignKey(CartCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_product_secondary_categories'
        unique_together = (('product', 'category'),)


class CartSizevariation(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cart_sizevariation'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoPostalcodesMexicoPostalcode(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    d_codigo = models.CharField(max_length=5)
    d_asenta = models.CharField(max_length=128)
    d_mnpio = models.CharField(db_column='D_mnpio', max_length=128)  # Field name made lowercase.
    d_ciudad = models.CharField(max_length=128, blank=True, null=True)
    c_estado = models.CharField(max_length=2)
    c_oficina = models.CharField(max_length=5)
    c_tipo_asenta = models.CharField(max_length=2)
    c_mnpio = models.CharField(max_length=3)
    id_asenta_cpcons = models.CharField(max_length=4)
    d_zona = models.CharField(max_length=10)
    c_cve_ciudad = models.CharField(max_length=2, blank=True, null=True)
    d_cp = models.CharField(db_column='d_CP', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'django_postalcodes_mexico_postalcode'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)

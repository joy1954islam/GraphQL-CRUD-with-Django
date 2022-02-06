import graphene
from graphene_django import DjangoObjectType
from .models import Category, Book, Grocery

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = [
            'id',
            'title'
        ]


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        field = [
            'id',
            'title',
            'author',
            'isbn',
            'pages',
            'price',
            'quantity',
            'description',
            'status',
            'date_created',
        ]

class GroceryType(DjangoObjectType):
    class Meta:
        model = Grocery
        field = [
            'id',
            'product_tag',
            'name',
            'category',
            'price',
            'quantity',
            'image_url',
            'status',
            'date_created',
        ]


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_books = graphene.List(BookType)
    all_groceries = graphene.List(GroceryType)
    single_categories = graphene.Field(CategoryType, category_id=graphene.Int())
    single_books = graphene.Field(BookType, book_id=graphene.Int())
    single_groceries = graphene.Field(GroceryType, geoceries_id=graphene.Int())

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_all_groceries(root, info):
        return Grocery.objects.all()

    def resolve_single_categories(root, info, category_id):
        return Category.objects.get(id=category_id)

    def resolve_single_books(root, info, book_id):
        return Book.objects.get(id=book_id)

    def resolve_single_groceries(root, info, geoceries_id):
        return Grocery.objects.get(pk=geoceries_id)


class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category(title=title)
        category.save()

        return CreateCategoryMutation(category=category)


class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title, id):
        category = Category.objects.get(id=id)
        category.title = title
        category.save()

        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()

        return

class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
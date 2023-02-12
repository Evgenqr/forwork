from rest_framework import serializers
from base.models import Document, Category, Departament, Law, Status


class DocumentSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='title')
    departament = serializers.SlugRelatedField(
        queryset=Departament.objects.all(), slug_field='title')
    status = serializers.SlugRelatedField(
        queryset=Status.objects.all(), slug_field='title')
    law = serializers.SlugRelatedField(
        queryset=Law.objects.all(), slug_field='shorttitle', many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Document
        fields = (
            'title', 'id', 'user', 'category', 'departament', 'status',
            'law', 'text')


class DocumentDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='title')
    departament = serializers.SlugRelatedField(
        queryset=Departament.objects.all(), slug_field='title')
    status = serializers.SlugRelatedField(
        queryset=Status.objects.all(), slug_field='title')
    law = serializers.SlugRelatedField(
        queryset=Law.objects.all(), slug_field='shorttitle', many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = Document
        fields = (
            'title', 'id', 'user', 'category', 'departament', 'status',
            'law', 'text')

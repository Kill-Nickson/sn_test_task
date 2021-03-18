from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body")

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "likes")

    def save(self, **kwargs):
        self.validated_data['user'] = kwargs['user']
        self.validated_data['liked'] = kwargs['liked']
        self.update(self.instance, self.validated_data)

    def update(self, instance, validated_data):
        cur_user = validated_data.pop('user')
        liked = validated_data.pop('liked')
        post = Post.objects.get(pk=instance.pk)

        if liked:
            post.likes.add(cur_user)
        else:
            post.likes.remove(cur_user)
        post.save()

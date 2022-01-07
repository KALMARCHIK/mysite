from rest_framework import serializers

from news.models import Post, Rubric, Comment, Like, Rating


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = 'like',


class PostRelationsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField(method_name='get_count_likes')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'rubric', 'created_at', 'user', 'likes', 'ratings', 'comments']

    def get_count_likes(self, post):
        likes = 0
        for like in post.likes.all():
            if like.like:
                likes += 1
            else:
                pass
        return likes

    def get_ratings(self, post):
        ratings = 0
        for rating in post.ratings.all():
            ratings += rating.rating
        ratings = ratings / len(post.ratings.all())
        return ratings


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'


class RubricPostSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Rubric
        fields = ['id', 'name', 'posts']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'user', 'post')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

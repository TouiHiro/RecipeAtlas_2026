
from django.shortcuts import render
from django.db.models import Count
from .models import Map
from recipes.models import Recipe


def map_view(request):

    region_id = request.GET.get('region_id')
    sort = request.GET.get('sort', 'new')

    selected_region = None
    recipes = Recipe.objects.none()
    recipe_count = 0

    # 表示件数
    limit = request.GET.get('limit', '10')

    if limit.isdecimal():
        limit = max(10, min(int(limit), 100))
    else:
        limit = 10

    # 地域情報を取得
    if region_id and region_id.isdecimal():

        selected_region = Map.objects.filter(
            region_id=int(region_id)
        ).first()

        if selected_region:

            # 地域別レシピを取得
            recipes = Recipe.objects.filter(
                region=selected_region
            ).select_related(
                'user',
                'user__region',
                'region'
            ).prefetch_related(
                'tag'
            ).annotate(
                favorite_count=Count(
                    'favorite_recipes',
                    distinct=True
                ),
                review_count=Count(
                    'reviews_recipe',
                    distinct=True
                )
            )

            # 人気順
            if sort == 'popular':
                recipes = recipes.order_by(
                    '-favorite_count', '-recipe_id'
                )

            # 口コミ件数順
            elif sort == 'review':
                recipes = recipes.order_by(
                    '-review_count', '-recipe_id'
                )

            # 新着順
            else:
                sort = 'new'
                recipes = recipes.order_by(
                    '-created_at', '-recipe_id'
                )

            recipe_count = recipes.count()
            recipes = recipes[:limit]

    context = {
        'selected_region': selected_region,
        'recipes': recipes,
        'recipe_count': recipe_count,
        'sort': sort,
        'limit': limit,
        'next_limit': min(limit + 10, 100),
        'has_more': recipe_count > limit and limit < 100,
    }

    return render(request, 'map.html', context)

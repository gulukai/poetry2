import os

from django.views import View
from .models import *

import json
from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpResponse, JsonResponse
from haystack.forms import ModelSearchForm
from haystack.query import EmptySearchQuerySet


# Create your views here.
# Poetry.objects.create(poetry_title='静夜思',poetry_author='李白',poetry_dynasty='唐',poetry_tag=('月亮','思乡'),
# poetry_text='窗前明月光，疑是地上霜。举头望明月，低头思故乡',poetry_translation='译文',
# poetry_annotation='注解',poetry_appreciation='赏析')

# {"所在小分类_1": "爱情",
# "题目": ["长干行二首"],
# "作者": ["唐朝:李白"],
# "正文": ["妾发初覆额，折花门前剧。", "郎骑竹马来，绕床弄青梅。", "同居长干里，两小无嫌猜，", "十四为君妇，羞颜未尝开。", "低头向暗壁，千唤不一回。", "十五始展眉，愿同尘与灰。", "常存抱柱信，岂上望夫台。", "十六君远行，瞿塘滟滪堆。", "五月不可触，猿声天上哀。", "门前迟行迹，一一生绿苔。", "苔深不能扫，落叶秋风早。", "八月胡蝶黄，双飞西园草。", "感此伤妾心，坐愁红颜老。", "早晚下三巴，预将书报家。", "相迎不道远，直至长风沙。", "忆妾深闺里，烟尘不曾识。", "嫁与长干人，沙头候风色。", "五月南风兴，思君下巴陵。", "八月西风起，想君发扬子。", "去来悲如何，见少离别多。", "湘潭几日到，妾梦越风波。", "昨夜狂风度，吹折江头树。", "淼淼暗无边，行人在何处。", "好乘浮云骢，佳期兰渚东。", "鸳鸯绿蒲上，翡翠锦屏中。", "自怜十五余，颜色桃花红。", "那作商人妇，愁水复愁风。\n      ", "\n      "],
# "译文": ["我的头发刚刚盖过额头，在门前折花做游戏。", "你骑着竹马过来，把弄着青梅，绕着床相互追逐。", "我们同在长干里居住，两个人从小都没什么猜忌。", "十四岁时嫁给你作妻子，害羞得没有露出过笑脸。", "低着头对着墙壁的暗处，一再呼唤也不敢回头。", "十五岁才舒展眉头，愿意永远和你在一起。", "常抱着至死不渝的信念，怎么能想到会走上望夫台。", "十六岁时你离家远行，要去瞿塘峡滟滪堆。", "五月水涨时，滟滪堆不可相触，两岸猿猴的啼叫声传到天上。", "门前是你离家时徘徊的足迹，渐渐地长满了绿苔。", "绿苔太厚，不好清扫，树叶飘落，秋天早早来到。", "八月里，黄色的蝴碟飞舞，双双飞到西园草地上。", "看到这种情景我很伤心，因而忧愁容颜衰老。", "无论什么时候你想下三巴回家，请预先把家书捎给我。", "迎接你不怕道路遥远，一直走到长风沙。", "想当初我在深闺的时候，不曾见识烟尘。", "可嫁给长干的男人后，整天在沙头等候风色。", "五月南风吹动的时候，想你正下巴陵。", "八月西风吹起的时候，想你正从扬子江出发。", "来来去去，聚少离多，悲伤几何？", "什么时候到湘潭呢？我最近天天梦见那里大起风波。", "昨夜又见狂风吹度，吹折了江头的大树。", "江水淼淼，昏暗无边，夫君啊你在何处？", "我将乘坐浮云骢，与你相会在兰渚东。", "鸳鸯嬉戏在绿蒲池上，翡翠鸟儿绣在锦屏当中。", "自顾自怜才十五岁多，面容正如桃花一般嫣红。", "哪里想到嫁为商人妇，既要愁水又要愁风。"],
# "注解": ["长干里：在今南京市，当年系船民集居之地，故《长干曲》多抒发船家女子的感情。", "抱柱信：典出出《庄子·盗跖篇》，写尾生与一女子相约于桥下，女子未到而突然涨水，尾生守信而不肯离去，抱着柱子被水淹死。", "滟滪堆：三峡之一瞿塘峡峡口的一块大礁石，农历五月涨水没礁，船只易触礁翻沉。", "天上哀：哀一作“鸣”。", "迟行迹：迟一作“旧”。生绿苔：绿一作“苍”。", "长风沙：地名，在今安徽省安庆市的长江边上，距南京约700里。", "忆妾深闺里：妾一作“昔”。", "沙头：沙岸上。风色：风向。", "下：一作“在”。巴陵：今湖南岳阳。", "发：出发。扬子：扬子渡。", "湘潭：泛指湖南一带。", "淼淼：形容水势浩大。", "浮云骢：骏马。西汉文帝有骏马名浮云。兰渚：生有兰草的小洲。", "翡翠：水鸟名。"],
# "赏析": ["诗人李白写过许多反映妇女生活的作品，《长干行两首》就是其中杰出的诗篇。", "长干是地名，在今江苏南京。乐府旧题有《长干曲》，郭茂倩《乐府诗集》卷七二载有古辞一首，五言四句，写一位少女驾舟采菱、途中遇潮的情景。与李白同时的崔颢有《长干曲》，崔国辅有《小长干曲》，也都是五言四旬的小乐府体，所描绘的都是长江中下游一带男女青年的生活场景。这些诗歌内容都较简单。李白《长干行》的篇幅加长了，内容也比较丰富。它以一位居住在长干里的商妇自述的口气，叙述了她的爱情生活，倾吐了对于远方丈夫的殷切思念。它塑造了一个具有丰富深挚的情感的少妇形象，具有动人的艺术力量。", "这是两首爱情叙事诗。第一首诗对商妇的各个生活阶段，通过生动具体的生活侧面的描绘，在读者面前展开了一幅幅鲜明生动的画面。诗人通过运用形象，进行典型的概括，开头的六句，婉若一组民间孩童嬉戏的风情画卷。“十四为君妇”以下八句，又通过心里描写生动细腻地描绘了小新娘出嫁后的新婚生活。在接下来的诗句中，更以浓重的笔墨描写闺中少妇的离别愁绪，诗情到此形成了鲜明转折。“门前迟行迹”以下八句，通过节气变化和不同景物的描写，将一个思念远行丈夫的少妇形象，鲜明地跃然于纸上。最后两句则透露了李白特有的浪漫主义色彩。这阕诗的不少细节描写是很突出而富于艺术效果的。如“妾发初覆额”以下几句，写男女儿童天真无邪的游戏动作，活泼可爱。“青梅竹马”成为至今仍在使用的成语。又如“低头向暗壁，千唤不一回”，写女子初结婚时的羞怯，非常细腻真切。诗人注意到表现女子不同阶段心理状态的变化，而没有作简单化的处理。再如“门前迟行迹，一一生绿苔”，“八月胡蝶黄，双飞西园草”，通过具体的景物描写，展示了思妇内心世界深邃的感情活动，深刻动人。", "第二首诗与第一首诗同是写商妇的爱情和离别的诗。第二首诗恰似第一首诗中的少妇风尘仆仆地划着小船来到长风沙的江边沙头上等候久别的丈夫。此诗在描述女子情感脉络上非常细密柔婉，像是山林中的清泉涓涓流畅而又还回曲折，给读者留下数不清的情韵，把少妇的闺怨描写得淋漓酣畅。这首诗中，诗人用“嫁与长干人，沙头候风色”两句便将女主人公的身世交代得清清楚楚。“五月南风兴”以下四句交代了诗中丈夫的行踪。“昨日狂风度，吹折江头树”则表现了她对夫婿安危的深切关怀，最后，“自怜十五余，颜色桃花江。那作商人妇，愁水复愁风”以少妇感怀身世的方式将满腔离愁别恨渲染得恰到好处。这首诗将南方女子温柔细腻的感情刻画得十分到位。全诗感情细腻，缠绵婉转，步步深入，语言坦白，音节和谐，格调清新隽永，也属诗歌艺术的上品。", "但是，与第一首诗相比起来，第二首诗显得要稍逊一筹。第二首诗与其他描写闺怨题材的诗一样，是从少妇时期入手， 而第一首诗却别出心裁，偏偏从童年时期的两小无猜写起，李白在此诗中打破了陈规，自出机杼。它通过描绘出的一副副生活场景 ，精心渲染环境气氛，使得人物性格更加生鲜自然，显示出完整性和独创性。一连串具有典型意义的生活片段和心理活动的描写，几乎显示了女主人公的一部性格发展史。这些是第二首诗所没有达到的艺术高度。", "透过第一首诗典型化的语言，塑造出了一个典型的商人小妇形象。这就是典型的塑造——典型环境中的典型人物。用“清水出芙蓉，天然去雕饰”来赞美这首诗是最贴切不过了，相形之下，第二首诗略显平庸，一则在于它的遣词用句没有前者的创新性，二者它的叙述方式没有摆脱掉其他相同题材诗歌的影子。它更加注重愁怨的描写，而第一首的最后两句“相迎不道远，直至长风沙”则带有一丝脱离封建礼教的解放色彩。因此，第一首诗塑造的人物更加鲜明饱满，更令读者喜爱。", "《长干行二首》的风格缠绵婉转，具有柔和深沉的美。商妇的爱情有热烈奔放的特点，同时又是那样地坚贞、持久、专一、深沉。她的丈夫是外出经商，并非奔赴疆场，吉凶难卜；因此，她虽也为丈夫的安危担心，但并不是摧塌心肺的悲恸。她的相思之情正如春蚕吐丝，绵绵不绝。这些内在的因素，决定了作品风格的深沉柔婉。 "],
# "标签": ["乐府", "妇女", "爱情", "叙事", "思念", "生活"]}

class getPoetry(View):
    def get(self, request):
        str1 = os.path.join(os.getcwd(), 'poetry\\ap\\ci.txt')
        strList = []
        with open(str1, 'r', encoding='utf-8') as f:
            str2 = f.read().replace("}", "}$").split("$")
            for sl in str2:
                strList.append(sl)
        for i in range(len(strList) - 1):
            jsonStr = json.loads(strList[i])
            text = "".join(jsonStr["正文"])  # 分出古诗的正文
            title = "".join(jsonStr["题目"])  # 分出古诗的题目
            translation = "".join(jsonStr["译文"])  # 分出古诗的译文
            annotation = "".join(jsonStr["注解"])  # 分出古诗的注解
            appreciation = "".join(jsonStr["赏析"])  # 分出古诗的赏析
            tag = tuple(jsonStr["标签"])  # 分出古诗的标签
            author = "".join(jsonStr["作者"]).split(":")[1]  # 分出古诗的作者
            dynasty = "".join(jsonStr["作者"]).split(":")[0]  # 分出古诗的朝代
            Poetry.objects.create(poetry_title=title, poetry_author=author, poetry_dynasty=dynasty, poetry_tag=tag,
                                  poetry_text=text, poetry_translation=translation,
                                  poetry_annotation=annotation, poetry_appreciation=appreciation)
        return HttpResponse("成功了！")


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


def basic_search(request, load_all=True, form_class=ModelSearchForm, searchqueryset=None, extra_context=None,
                 results_per_page=None):
    query = ''
    results = EmptySearchQuerySet()
    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        result = {"code": 404, "msg": 'No file found！', "data": []}
        return HttpResponse(json.dumps(result), content_type="application/json")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }
    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)
    jsondata = []
    print(len(page.object_list))
    for result in page.object_list:
        tagList = []
        tag = Poetry.objects.get(poetry_no=result.object.poetry_no).poetry_tag.all()
        for t in tag:
            tagList.append(t.tag_name)
        # 返回的响应
        data = {
            'no': result.object.poetry_no,
            'title': result.object.poetry_title,
            'author': result.object.poetry_author.author_name,
            'dynasty': result.object.poetry_dynasty.dynasty_name,
            'text': result.object.poetry_text,
            'translation': result.object.poetry_translation,
            'annotation': result.object.poetry_annotation,
            'appreciation': result.object.poetry_appreciation,
            'tag': tuple(tagList)
        }
        jsondata.append(data)
        tagList.clear()
    if len(jsondata) == 0:
        result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
    else:
        result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
    return JsonResponse(result, content_type="application/json")


class postAuthor(View):
    def get(self, request):
        str1 = os.path.join(os.getcwd(), 'poetry\\ar\\jin_author.txt')
        strList = []
        with open(str1, 'r', encoding='utf-8') as f:
            str2 = f.read().replace("}", "}$").split("$")
            for sl in str2:
                strList.append(sl)
        for i in range(len(strList) - 1):
            jsonStr = json.loads(strList[i])
            name = "".join(jsonStr["author_name"])  # 分出作者的姓名
            introduce = "".join(jsonStr["author_introduce"])  # 分出作者的介绍
            try:
                AuthorDetails.objects.get(ad_name=name, ad_introduce=introduce)
            except AuthorDetails.DoesNotExist:
                AuthorDetails.objects.create(ad_name=name, ad_introduce=introduce)
        return HttpResponse("加完了！")


def getAuthorById(request, num):
    num = int(num)
    poetry = Poetry.objects.get(poetry_no=num)
    data = {
        "no": poetry.poetry_no,
        "dynasty": poetry.poetry_dynasty.dynasty_name,
        "author": poetry.poetry_author.author_name,
        "text": poetry.poetry_text
    }
    result = {"code": 200, "msg": "Search successfully!", "data": data}
    return JsonResponse(result, content_type="application/json")


# http://www.gulukai.cn/poetry/getpoetry/?p1=search&p2=title
class Optimization_Url(View):
    def get(self, request):
        p1 = request.GET.get("p1")
        p2 = request.GET.get("p2")
        if p1 == "author":
            num = Author.objects.filter(author_name=p2)
            if len(num) != 0:
                num2 = num[0].author_no
                poetries = Poetry.objects.filter(poetry_author=num2)
                jsondata = []
                tagList = []
                for po in poetries:
                    tag = Poetry.objects.get(poetry_no=po.poetry_no).poetry_tag.all()
                    for t in tag:
                        tagList.append(t.tag_name)
                    # 返回的响应
                    data = {
                        'no': po.poetry_no,
                        'title': po.poetry_title,
                        'author': po.poetry_author.author_name,
                        'dynasty': po.poetry_dynasty.dynasty_name,
                        'text': po.poetry_text,
                        'translation': po.poetry_translation,
                        'annotation': po.poetry_annotation,
                        'appreciation': po.poetry_appreciation,
                        'tag': tuple(tagList)
                    }
                    jsondata.append(data)
                    tagList.clear()
                if len(jsondata) == 0:
                    result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                else:
                    result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
                return JsonResponse(result, content_type="application/json")
            else:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        elif p1 == "title":
            poetries = Poetry.objects.filter(poetry_title=p2)
            print(poetries)
            if len(poetries) != 0:
                jsondata = []
                tagList = []
                for po in poetries:
                    tag = Poetry.objects.get(poetry_no=po.poetry_no).poetry_tag.all()
                    print(po.poetry_no)
                    for t in tag:
                        tagList.append(t.tag_name)
                    # 返回的响应
                    data = {
                        'no': po.poetry_no,
                        'title': po.poetry_title,
                        'author': po.poetry_author.author_name,
                        'dynasty': po.poetry_dynasty.dynasty_name,
                        'text': po.poetry_text,
                        'translation': po.poetry_translation,
                        'annotation': po.poetry_annotation,
                        'appreciation': po.poetry_appreciation,
                        'tag': tuple(tagList)
                    }
                    jsondata.append(data)
                    tagList.clear()
                if len(jsondata) == 0:
                    result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                else:
                    result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
                return JsonResponse(result, content_type="application/json")
            else:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        elif p1 == "dynasty":
            num = Dynasty.objects.filter(dynasty_name=p2)
            if len(num) != 0:
                num2 = num[0].dynasty_no
                poetries = Poetry.objects.filter(poetry_dynasty=num2)
                jsondata = []
                for po in poetries:
                    tagList = []
                    tag = Poetry.objects.get(poetry_no=po.poetry_no).poetry_tag.all()
                    for t in tag:
                        tagList.append(t.tag_name)
                    # 返回的响应
                    data = {
                        'no': po.poetry_no,
                        'title': po.poetry_title,
                        'author': po.poetry_author.author_name,
                        'dynasty': po.poetry_dynasty.dynasty_name,
                        'text': po.poetry_text,
                        'translation': po.poetry_translation,
                        'annotation': po.poetry_annotation,
                        'appreciation': po.poetry_appreciation,
                        'tag': tuple(tagList)
                    }
                    jsondata.append(data)
                if len(jsondata) == 0:
                    result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                else:
                    result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
                return JsonResponse(result, content_type="application/json")
            else:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        elif p1 == "tag":
            try:
                poetries = Tag.objects.get(tag_name=p2).poetry_set.all()
                jsondata = []
                tagList = []
                for po in poetries:
                    tag = Poetry.objects.get(poetry_no=po.poetry_no).poetry_tag.all()
                    for t in tag:
                        tagList.append(t.tag_name)
                    # 返回的响应
                    data = {
                        'no': po.poetry_no,
                        'title': po.poetry_title,
                        'author': po.poetry_author.author_name,
                        'dynasty': po.poetry_dynasty.dynasty_name,
                        'text': po.poetry_text,
                        'translation': po.poetry_translation,
                        'annotation': po.poetry_annotation,
                        'appreciation': po.poetry_appreciation,
                        'tag': tuple(tagList)
                    }
                    jsondata.append(data)
                    tagList.clear()
                if len(jsondata) == 0:
                    result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                else:
                    result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
                return JsonResponse(result, content_type="application/json")
            except Tag.DoesNotExist:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        elif p1 == "getauthor":
            try:
                authors = AuthorDetails.objects.get(ad_name=p2)
                data = {
                    'no': authors.ad_no,
                    'name': authors.ad_name,
                    'introduce': authors.ad_introduce,
                }
                result = {"code": 200, "msg": 'Search successfully！', "data": data}
                return JsonResponse(result, content_type="application/json")
            except AuthorDetails.DoesNotExist:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        elif p1 == "search":
            if p2 == "author":
                authorList = []
                authors = Author.objects.all()
                for ar in authors:
                    authorList.append(ar.author_name)
                data = {
                    "authors": authorList
                }
                result = {"code": 200, "msg": 'Search successfully！', "data": data}
                return JsonResponse(result, content_type="application/json")
            elif p2 == "title":
                titleList = []
                titles = Title.objects.all()
                for t in titles:
                    titleList.append(t.title_name)
                data = {
                    "titles": titleList
                }
                result = {"code": 200, "msg": 'Search successfully！', "data": data}
                return JsonResponse(result, content_type="application/json")
            elif p2 == "tag":
                tagList = []
                tags = Tag.objects.all()
                for tag in tags:
                    tagList.append(tag.tag_name)
                data = {
                    "tags": tagList
                }
                result = {"code": 200, "msg": 'Search successfully！', "data": data}
                return JsonResponse(result, content_type="application/json")
            else:
                result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
                return JsonResponse(result, content_type="application/json")
        else:
            result = {"code": 200, "msg": 'Search successfully！', "data": "None"}
            return JsonResponse(result, content_type="application/json")

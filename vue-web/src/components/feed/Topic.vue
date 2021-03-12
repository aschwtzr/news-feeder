<template>
  <div>
    <p v-if="!hide" class="title is-4">
      {{topic.title}}
    <!-- </strong> -->
    <div class="card">
      <header class="card-header" @click="hide = !hide" style="cursor: pointer;">
        <p class="card-header-title">
          {{ hide ? topic.title : ''}}
        <div class="card-header-icon">
          <span class="icon" :id="`${topicId}-${hide}`">
            <i
              v-if="hide"
              class="fas fa-angle-right"
              aria-hidden="true"
            />
            <i
              v-else
              class="fas fa-angle-down"
              aria-hidden="true"
            />
          </span>
        </div>
      </header>
      <div class="card-content" :style="hide ? 'display: none;' : ''">
        <div class="media">
          <div class="media-left" style="width: 30vw;">
            <figure class="image is-square">
              <img :src="imageURL" alt="Placeholder image">
            </figure>
            {{templateId}}
          </div>
          <div class="media-content">
            <p class="subtitle is-6">
              {{topic.topic_sum}}
            </p>
            <div class="subtitle is-6 topic__keyword-container">
              <div
                v-for="(keyword, index) in topic.keywords"
                :key="`${keyword}-${index}-${topicId}`"
                @click="setSelectedKeywords(keyword)"
                >
                <button class="button is-white">{{`${keyword} `}}</button>
              </div>
            </div>
          </div>
        </div>
        <em :style="!groupedBySource ? 'display: none;': 'font-weight: strong'">
          <div class="subtitle is-6">keywords:  </div>
        </em>
        <div
          v-for="(article, index) in topic.articles"
          :key="`${article.keywords.slice(0,3).join('-')}-${index}`"
          >
          <article-card
            :showSourceInHeader="!groupedBySource"
            :source="article.source"
            :title="article.title"
            :url="article.url"
            :content="article.preview"
            :date="article.date"
            :id="article.id"
            :keywords="article.keywords"
            :summary="article.summary || false"
            />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapMutations } from 'vuex';
import ArticleCard from '@/components/article/ArticleCard.vue';
import { getTopicImage } from '@/util/api';

export default {
  name: 'Topic',
  props: ['topic', 'groupedBySource'],
  data() {
    return {
      imageURL: '',
      templateId: 0,
      hide: false,
    };
  },
  components: {
    ArticleCard,
  },
  methods: {
    ...mapMutations({
      setSelectedKeywords: 'feeds/setSelectedKeywords',
    }),
    setImageUrl(url) {
      this.imageURL = url;
    },
  },
  computed: {
    topicId() {
      return `${this.topic.keywords[0]}-${this.topic.articles[0].id}`;
    },
    headerIconClass() {
      return `fas fa-angle-${this.hide ? 'down' : 'right'}`;
    },
  },
  async mounted() {
    const { setImageUrl } = this;
    const keywords = [...this.topic.keywords];
    const idIdx = Math.floor(Math.random() * Math.floor(99));
    const half = Math.ceil(keywords.length / 2);
    const firstHalf = keywords.splice(0, half).join(' ');
    const secondHalf = keywords.splice(-half).join(' ');
    const ids = [112126428, 181913649, 87743020, 438680, 129242436, 61579,
      124822590, 102156234, 93895088, 101470, 1035805, 131087935, 4087833,
      89370399, 61520, 91538330, 217743513, 188390779, 119139145, 97984,
      61532, 5496396, 155067746, 8072285, 61585, 114585149, 100777631, 61539,
      21735, 124055727, 123999232, 27813981, 28251713, 222403160, 178591752,
      247375501, 61527, 134797956, 101288, 6235864, 563423, 61546, 61582,
      91545132, 101511, 405658, 61533, 148909805, 61556, 16464531,
      226297822, 14371066, 1509839, 135256802, 175540452, 101287, 235589,
      84341851, 100947, 14230520, 61544, 135678846, 61516, 80707627, 245898,
      161865971, 252600902, 196652226, 101440, 132769734, 922147, 61580, 180190441,
      3218037, 40945639, 259680, 101910402, 101716, 109765, 9440985, 61581,
      56225174, 55311130, 110163934, 12403754, 79132341, 195389, 259237855,
      766986, 163573, 21604248, 444501, 100955, 460541, 718432,
      124212, 13757816, 61583];
    this.templateId = ids[idIdx];
    const params = {
      username: 'newssummAPI',
      password: 'MemeAPI$131990!',
      template_id: ids[idIdx],
      text0: firstHalf,
      text1: secondHalf,
    };
    await getTopicImage(params).then((res) => {
      if (res.data.url) {
        setImageUrl(res.data.url);
      } else setImageUrl('https://i.imgflip.com/51dvy5.jpg');
    });
  },
};
</script>
<style>
  .topic__keyword-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
</style>

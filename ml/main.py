import re

import pickle
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer, util


def clear_text(text):
    text = text.lower()
    text = re.sub('[^а-я ]', ' ', text)
    text = ' '.join(text.split())
    return text


def get_related(ids: list, descriptions: list, top_k: int = 5) -> pd.DataFrame:
    """
    Вычисляет ближайшие события исходя из близости по векторному пространству
    :param ids[list] - id событий
    :param descriptions[list] - описание событий
    :param top_k - количество близких событий
    :return pd.DataFrame - датафрейм близких событий
    """

    ids = np.array(ids)
    texts = [clear_text(text) for text in descriptions]
    # load andd apply model
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    paraphrases = util.paraphrase_mining(model, texts, show_progress_bar=True, top_k=5)
    paraphrases = np.array(paraphrases)
    df_paraphrases = pd.DataFrame(paraphrases, columns=['score', 'original_project', 'related_project'])
    df_paraphrases1 = df_paraphrases.copy()
    df_paraphrases1.columns = ['score', 'related_project', 'original_project']
    answer = pd.concat((df_paraphrases, df_paraphrases1)).sort_values(by='score', ascending=False).groupby(
        'original_project').head(5)
    answer.original_project = ids[answer.original_project.values.astype(int)]
    answer.related_project = ids[answer.related_project.values.astype(int)]

    return answer


def calculate_recommendation_users_and_projects(projects, users):
    """
    Возвращает рекомендуемые проекты для юзеров (recommended_projects)
    и рекомендуемых юзеров для проекта (recommended_members) - именно в таком порядке
    :param projects[pd.DataFrame] - датафрейм с столбцами проекта 'id', 'category', 'open_vacancy' - открытая роль в команде (если есть) каждая открытая вакансия - отдельная строчка
    :param users[pd.DataFrame] - датафрейм с столбцами пользователя 'id', 'role' - желаемая роль, 'interests' - формируемая объединением interests и hidden_interests пользователя

    Инструкция по данным:
        project: искомые вакансии (кого ищут - дизанер, менеджер и т.п.)
    """

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    frame = users.merge(projects, left_on='position', right_on = 'open_vacancy', suffixes = ['_user', '_project'])

    # Получаем эмбединги
    embeddings1 = model.encode(frame.interest.apply(lambda x: clear_text(' '.join(x))).values, convert_to_tensor=True)
    embeddings2 = model.encode(frame.category.apply(lambda x: clear_text(x)).values, convert_to_tensor=True)
    # Считаем схожесть по дистанции косинуса
    sims = []
    cos_distance = util.cos_sim(embeddings1, embeddings2)
    for i in range(frame.shape[0]):
        sims.append(float(cos_distance[i, i].numpy()))
    frame['cosine'] = sims
    frame = frame.loc[:, ['id_user', 'id_project', 'cosine']].sort_values(by = 'cosine', ascending = False)
    # считаем метрику схожести для user-project и оставляем топ n релевантных
    return frame.groupby('id_user').head(5), frame.groupby('id_project').head(5)


def get_top_tags(text: pd.DataFrame, categories: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    """
    Получает топ-5 категорий, близких к описанию проекта

    :param text[pd.DataFrame] - описание или другой текст проекта, к которому необходимо подобрать категорию
    :param categories[pd.DataFrame] - список категорий, с которым необходимо сравнить
    :param top_k[int] - количество возвращаемых категорий
    :return pd.DataFrame - score-tag фрейм с отсортированными категориями
    """
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Получаем эмбединги
    embeddings1 = model.encode(text.text.apply(lambda x: clear_text(x)), convert_to_tensor=True)
    embeddings2 = model.encode(categories.name, convert_to_tensor=True)

    # Считаем схожесть по дистанции косинуса
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    # Сгенерировать фрейм с очками и названием категорий
    top_tags_t = pd.DataFrame()
    top_tags_t['project_id'] = np.array([[id] * cosine_scores.shape[1] for id in text.id]).ravel()
    top_tags_t['score'] = np.round(cosine_scores, 2).ravel()
    top_tags_t['tag'] = list(categories.id) * cosine_scores.shape[0]
    return top_tags_t.sort_values(by='score', ascending=False).groupby('project_id').head(top_k)
        
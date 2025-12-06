export const mockMovies = [
  {
    id: 1,
    title: '인터스텔라',
    original_title: 'Interstellar',
    poster_path: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    release_date: '2014-11-07',
    runtime: 169,
    genres: ['SF', '드라마', '모험'],
    overview: '세계 각국의 정부와 경제가 완전히 붕괴된 미래가 다가온다. 지구에서의 삶은 불가능해지고, 인류는 멸종 위기에 처한다.',
    stats: {
      avg_rating: 4.6,
      rating_count: 15420,
      rating_distribution: {
        '5.0': 8234,
        '4.0': 4521,
        '3.0': 1892,
        '2.0': 521,
        '1.0': 252
      }
    },
    tmdb_rating: 8.4,
    imdb_rating: 8.7
  },
  {
    id: 2,
    title: '기생충',
    original_title: 'Parasite',
    poster_path: 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
    release_date: '2019-05-30',
    runtime: 132,
    genres: ['스릴러', '드라마', '코미디'],
    overview: '전원 백수인 기택의 가족이 고급 주택에 사는 부유한 박씨 가족에게 들어가게 되면서 벌어지는 이야기.',
    stats: {
      avg_rating: 4.7,
      rating_count: 23891,
      rating_distribution: {
        '5.0': 12453,
        '4.0': 7823,
        '3.0': 2341,
        '2.0': 892,
        '1.0': 382
      }
    },
    tmdb_rating: 8.5,
    imdb_rating: 8.5
  }
];

export const mockUsers = [
  {
    id: 1,
    username: '영화매니아',
    email: 'movie@example.com',
    profile_image: 'https://i.pravatar.cc/150?img=1',
    created_at: '2023-01-15T00:00:00Z'
  },
  {
    id: 2,
    username: '시네필',
    email: 'cinephile@example.com',
    profile_image: 'https://i.pravatar.cc/150?img=2',
    created_at: '2023-03-20T00:00:00Z'
  },
  {
    id: 3,
    username: '영화광',
    email: 'movielover@example.com',
    profile_image: 'https://i.pravatar.cc/150?img=3',
    created_at: '2023-05-10T00:00:00Z'
  }
];

export const mockComments = [
  {
    id: 1,
    user_id: 2,
    movie_id: 1,
    rating: 5.0,
    review_content: '놀란의 최고 걸작. 시간과 차원을 넘나드는 이야기가 정말 감동적이었습니다. 과학적 고증도 훌륭하고, 부녀간의 사랑 이야기도 너무 좋았어요.',
    spoiler: false,
    created_at: '2024-12-01T10:30:00Z',
    username: '시네필',
    profile_image: 'https://i.pravatar.cc/150?img=2',
    likes_count: 24,
    isLiked: false
  },
  {
    id: 2,
    user_id: 3,
    movie_id: 1,
    rating: 4.5,
    review_content: '마지막 장면에서 쿠퍼가 머피를 다시 만나는 순간은 정말... 눈물이 났습니다. 타임패러독스도 완벽하게 해결했어요.',
    spoiler: true,
    created_at: '2024-11-28T15:20:00Z',
    username: '영화광',
    profile_image: 'https://i.pravatar.cc/150?img=3',
    likes_count: 15,
    isLiked: false
  },
  {
    id: 3,
    user_id: 1,
    movie_id: 2,
    rating: 5.0,
    review_content: '한국 영화 역사에 길이 남을 작품. 계급 사회에 대한 날카로운 풍자와 반전이 정말 충격적이었습니다.',
    spoiler: false,
    created_at: '2024-11-25T18:45:00Z',
    username: '영화매니아',
    profile_image: 'https://i.pravatar.cc/150?img=1',
    likes_count: 42,
    isLiked: false
  }
];

export const mockUserStats = {
  total_ratings: 127,
  avg_rating: 4.2,
  high_ratings: 89,
  low_ratings: 12,
  liked_movies: 34,
  total_comments: 56
};

export const mockUserRatings = [
  {
    id: 1,
    user_id: 1,
    movie_id: 1,
    rating: 5.0,
    watched_at: '2024-11-20T00:00:00Z',
    title: '인터스텔라',
    poster_path: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    review_content: '최고의 SF 영화'
  },
  {
    id: 2,
    user_id: 1,
    movie_id: 2,
    rating: 4.5,
    watched_at: '2024-11-15T00:00:00Z',
    title: '기생충',
    poster_path: 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
    review_content: '완벽한 연출과 연기'
  }
];

export const mockLikedMovies = [
  {
    id: 1,
    title: '인터스텔라',
    poster_path: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    release_date: '2014-11-07',
    liked_at: '2024-11-20T00:00:00Z'
  },
  {
    id: 2,
    title: '기생충',
    poster_path: 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
    release_date: '2019-05-30',
    liked_at: '2024-11-15T00:00:00Z'
  }
];

export const mockUserComments = [
  {
    id: 1,
    user_id: 1,
    movie_id: 1,
    movie_title: '인터스텔라',
    movie_poster: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    rating: 5.0,
    content: '최고의 SF 영화. 과학적 고증과 감동을 동시에 잡은 명작입니다.',
    created_at: '2024-11-20T00:00:00Z',
    likes_count: 12
  },
  {
    id: 2,
    user_id: 1,
    movie_id: 2,
    movie_title: '기생충',
    movie_poster: 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
    rating: 4.5,
    content: '봉준호 감독의 완벽한 연출. 계급 사회를 날카롭게 풍자한 걸작.',
    created_at: '2024-11-15T00:00:00Z',
    likes_count: 8
  }
];

export const mockUserTaste = {
  favoriteGenres: [
    { genre: 'SF', count: 23, avg_rating: 4.5 },
    { genre: '드라마', count: 45, avg_rating: 4.3 },
    { genre: '스릴러', count: 31, avg_rating: 4.4 }
  ],
  tendency: {
    isStrict: false,
    positiveRatio: 0.72,
    avgRating: 4.2
  }
};
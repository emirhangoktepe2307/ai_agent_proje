<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Hikaye Oluşturucu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .glass-effect {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .input-focus {
            transition: all 0.3s ease;
        }
        .input-focus:focus {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .btn-hover {
            transition: all 0.3s ease;
        }
        .btn-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .story-card {
            transition: all 0.3s ease;
        }
        .story-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            z-index: 1000;
        }
        .loading-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">
    <!-- Loading Overlay -->
    <div id="loading" class="loading">
        <div class="loading-content">
            <div class="spinner"></div>
            <p class="text-xl font-semibold">Hikaye oluşturuluyor...</p>
        </div>
    </div>

    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="glass-effect rounded-2xl p-6 mb-8 flex justify-between items-center">
            <h1 class="text-2xl md:text-3xl font-bold text-gray-800">Hikaye Oluşturucu</h1>
            <form action="{{ route('logout') }}" method="POST" class="inline">
                @csrf
                <button type="submit" class="btn-hover px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700">
                    Çıkış Yap
                </button>
            </form>
        </div>

        <!-- Story Creation Form -->
        <div class="glass-effect rounded-2xl p-6 mb-8">
            <form id="storyForm" class="space-y-6">
                @csrf
                <div>
                    <label for="prompt" class="block text-sm font-medium text-gray-700 mb-2">Hikaye Konusu</label>
                    <textarea id="prompt" name="prompt" rows="4" required
                        class="input-focus w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="Hikayenizin konusunu yazın..."></textarea>
                </div>

                <div class="flex flex-wrap gap-4">
                    <div class="flex-1 min-w-[200px]">
                        <label for="genre" class="block text-sm font-medium text-gray-700 mb-2">Tür</label>
                        <select id="genre" name="genre" required
                            class="input-focus w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                            <option value="">Tür seçin</option>
                            <option value="fantasy">Fantastik</option>
                            <option value="scifi">Bilim Kurgu</option>
                            <option value="mystery">Gizem</option>
                            <option value="romance">Romantik</option>
                        </select>
                    </div>

                    <div class="flex-1 min-w-[200px]">
                        <label for="length" class="block text-sm font-medium text-gray-700 mb-2">Uzunluk</label>
                        <select id="length" name="length" required
                            class="input-focus w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                            <option value="">Uzunluk seçin</option>
                            <option value="short">Kısa</option>
                            <option value="medium">Orta</option>
                            <option value="long">Uzun</option>
                        </select>
                    </div>
                </div>

                <button type="submit" 
                    class="btn-hover w-full md:w-auto px-8 py-3 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Hikaye Oluştur
                </button>
            </form>
        </div>

        <!-- Story List -->
        <div id="storyList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            @foreach($stories ?? [] as $story)
            <div class="story-card glass-effect rounded-2xl p-6">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ $story->title }}</h3>
                <p class="text-gray-600 mb-4">{{ Str::limit($story->content, 150) }}</p>
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">{{ $story->created_at->diffForHumans() }}</span>
                    <button class="btn-hover px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-100 rounded-lg hover:bg-indigo-200">
                        Devamını Oku
                    </button>
                </div>
            </div>
            @endforeach
        </div>
    </div>

    <script>
        document.getElementById('storyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loading = document.getElementById('loading');
            const storyList = document.getElementById('storyList');
            
            try {
                loading.style.display = 'block';
                
                const formData = new FormData(e.target);
                const response = await fetch('{{ route("generate-story") }}', {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': '{{ csrf_token() }}',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: formData.get('prompt'),
                        genre: formData.get('genre'),
                        length: formData.get('length')
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Yeni hikayeyi listeye ekle
                    const storyHtml = `
                        <div class="story-card glass-effect rounded-2xl p-6">
                            <h3 class="text-xl font-semibold text-gray-800 mb-2">${data.story.title}</h3>
                            <p class="text-gray-600 mb-4">${data.story.content}</p>
                            <div class="flex justify-between items-center">
                                <span class="text-sm text-gray-500">Az önce</span>
                                <button class="btn-hover px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-100 rounded-lg hover:bg-indigo-200">
                                    Devamını Oku
                                </button>
                            </div>
                        </div>
                    `;
                    
                    storyList.insertAdjacentHTML('afterbegin', storyHtml);
                    e.target.reset();
                } else {
                    alert('Hikaye oluşturulurken bir hata oluştu.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Bir hata oluştu. Lütfen tekrar deneyin.');
            } finally {
                loading.style.display = 'none';
            }
        });
    </script>
</body>
</html> 
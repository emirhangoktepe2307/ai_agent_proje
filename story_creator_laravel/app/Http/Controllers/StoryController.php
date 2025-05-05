<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class StoryController extends Controller
{
    public function index()
    {
        // Örnek hikayeler (gerçek uygulamada veritabanından çekilecek)
        $stories = collect([
            (object)[
                'title' => 'Örnek Hikaye 1',
                'content' => 'Bu bir örnek hikaye içeriğidir. Gerçek uygulamada veritabanından gelecektir.',
                'created_at' => now()
            ],
            (object)[
                'title' => 'Örnek Hikaye 2',
                'content' => 'Bu başka bir örnek hikaye içeriğidir. Gerçek uygulamada veritabanından gelecektir.',
                'created_at' => now()->subHours(2)
            ]
        ]);

        return view('story', compact('stories'));
    }

    public function generate(Request $request)
    {
        $request->validate([
            'prompt' => 'required|string|min:10',
            'genre' => 'required|string',
            'length' => 'required|string'
        ]);

        // Burada AI ile hikaye oluşturma işlemi yapılacak
        // Şimdilik örnek bir yanıt döndürelim
        $story = [
            'title' => 'Oluşturulan Hikaye',
            'content' => 'Bu bir örnek hikaye içeriğidir. Gerçek uygulamada AI tarafından oluşturulacaktır.',
            'created_at' => now()
        ];

        // Başarılı yanıt döndür
        return response()->json([
            'success' => true,
            'story' => $story
        ]);
    }
} 
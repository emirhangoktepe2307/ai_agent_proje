<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function showLogin()
    {
        // Şimdilik her zaman login sayfasını göster
        return view('auth.login');
    }

    public function login(Request $request)
    {
        // Şimdilik direkt story sayfasına yönlendir
        return redirect()->route('story');
    }

    public function logout(Request $request)
    {
        return redirect()->route('login');
    }
} 
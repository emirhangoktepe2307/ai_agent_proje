<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\StoryController;

// Ana sayfa yönlendirmesi
Route::get('/', function () {
    return redirect('/login');
});

// Auth routes
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login'])->name('login.post');
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Story routes - şimdilik korumasız
Route::get('/story', [StoryController::class, 'index'])->name('story');
Route::post('/generate-story', [StoryController::class, 'generate'])->name('generate-story');

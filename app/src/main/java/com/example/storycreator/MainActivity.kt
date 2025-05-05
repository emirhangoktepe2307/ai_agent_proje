package com.example.storycreator

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebSettings
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.CookieManager
import android.util.Log
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)
        setupWebView()
    }

    private fun setupWebView() {
        // Cookie yönetimini etkinleştir
        CookieManager.getInstance().apply {
            setAcceptCookie(true)
            setAcceptThirdPartyCookies(webView, true)
            removeAllCookies(null)
            flush()
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                Log.e("WebView", "Hata: ${error?.description}")
                Log.e("WebView", "URL: ${request?.url}")
                Log.e("WebView", "Method: ${request?.method}")
                Log.e("WebView", "Headers: ${request?.requestHeaders}")
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                Log.d("WebView", "Sayfa yüklendi: $url")
                Log.d("WebView", "Cookies: ${CookieManager.getInstance().getCookie(url)}")
                
                // Eğer login sayfasındaysak ve cookie'ler varsa, story sayfasına yönlendir
                if (url?.contains("/login") == true) {
                    val cookies = CookieManager.getInstance().getCookie(url)
                    if (cookies?.contains("laravel_session") == true) {
                        view?.loadUrl("http://10.0.2.2:8000/story")
                    }
                }
            }

            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                Log.d("WebView", "URL yükleniyor: $url")
                url?.let { view?.loadUrl(it) }
                return true
            }
        }

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            setSupportZoom(true)
            builtInZoomControls = true
            displayZoomControls = false
            loadWithOverviewMode = true
            useWideViewPort = true
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            cacheMode = WebSettings.LOAD_NO_CACHE
            allowFileAccess = true
            allowContentAccess = true
            databaseEnabled = true
            setAppCacheEnabled(true)
            setAppCachePath(applicationContext.cacheDir.absolutePath)
            userAgentString = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        }

        // Emülatör için özel IP adresi
        val url = "http://10.0.2.2:8000/login"
        Log.d("WebView", "Başlangıç URL'si yükleniyor: $url")
        webView.loadUrl(url)
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
} 
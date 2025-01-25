<!DOCTYPE html>
<html>
<head>
    <title>{{get('title', ' ')}} - Tarique's Running Heatmap</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark py-0">
        <div class="container-fluid">
            <a class="navbar-brand py-2 my-0" href="/">Tarique's Running Heatmap</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/"><i class="bi bi-house-fill"></i></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/heatmap">Heatmap</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle py-2 my-0" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Sync
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/sync">Full Sync</a></li>
                            <li><a class="dropdown-item" href="/sync/inc">Incremental Sync</a></li>
                        </ul>
                    </li>                    
                </ul>
            </div>
        </div>
    </nav>
    
    {{!base}}
    
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container text-center">
            <p class="text-muted mb-0">&copy; 2025 Strava Heatmap Project</p>
        </div>
    </footer>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Navigator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; color: #333; }
        h1 { font-size: 1.5rem; border-bottom: 2px solid #ccc; padding-bottom: 10px; }
        ul { list-style: none; padding: 0; }
        li { padding: 8px 12px; margin: 4px 0; background: #fff; border: 1px solid #ddd; border-radius: 4px; display: flex; align-items: center; }
        li:hover { background: #f0f0f5; }
        a { text-decoration: none; color: #0066cc; display: flex; align-items: center; width: 100%; }
        .folder { font-weight: bold; color: #d97706; }
        .file { color: #2563eb; }
    </style>
</head>
<body>

    <h1>Current Directory Navigator</h1>
    
    <?php
    // Get current directory or requested sub-directory safely
    $base_dir = '.'; 
    $request_path = isset($_GET['dir']) ? $_GET['dir'] : '';
    
    // Clean path to prevent security issues (directory traversal)
    $current_dir = realpath($base_dir . '/' . $request_path);
    
    if ($current_dir === false || strpos($current_dir, realpath($base_dir)) !== 0) {
        $current_dir = realpath($base_dir);
    }
    
    echo "<p><strong>Path:</strong> /" . htmlspecialchars($request_path) . "</p>";
    
    // Show a back button if inside a subfolder
    if ($request_path !== '') {
        $parent_path = dirname($request_path);
        if ($parent_path === '.') $parent_path = '';
        echo '<p><a href="?dir=' . urlencode($parent_path) . '">📁 <strong>[Up one level]</strong></a></p>';
    }
    
    // Scan directory
    $items = scandir($current_dir);
    
    echo "<ul>";
    foreach ($items as $item) {
        // Skip hidden files and self/parent pointers
        if ($item === '.' || $item === '..') continue;
        if ($item === 'index.php' || $item === '.htaccess') continue; // Hide navigator itself if wanted
        
        $item_path = $current_dir . '/' . $item;
        $relative_path = ($request_path === '') ? $item : $request_path . '/' . $item;
        
        if (is_dir($item_path)) {
            // It's a folder
            echo '<li><a class="folder" href="?dir=' . urlencode($relative_path) . '">📁 ' . htmlspecialchars($item) . '</a></li>';
        } else {
            // It's a file
            echo '<li><a class="file" href="' . htmlspecialchars($relative_path) . '" target="_blank">📄 ' . htmlspecialchars($item) . '</a></li>';
        }
    }
    echo "</ul>";
    ?>

</body>
</html>

<?php
declare(strict_types=1);

// Reads from the environment (set in docker-compose) so the same code runs
// unchanged in local Docker dev and production — falls back to XAMPP/MAMP-
// style local defaults for running this outside Docker entirely.
$host = getenv('BPF_DB_HOST') ?: 'localhost';
$database = getenv('BPF_DB_NAME') ?: 'bpf_scorecard';
$username = getenv('BPF_DB_USER') ?: 'root';
$password = getenv('BPF_DB_PASSWORD') ?: 'root';

$dsn = sprintf(
    'mysql:host=%s;dbname=%s;charset=utf8mb4',
    $host,
    $database
);

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

$pdo = new PDO(
    $dsn,
    $username,
    $password,
    $options
);
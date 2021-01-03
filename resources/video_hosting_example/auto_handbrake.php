<?php
$video_directory = '/raid/video_game_clips';
$encoded_directory = 'h264_encoded';

$results = scandir($video_directory);
$now = new DateTime();

// Automatically script handbrake to encode files as h264 if they are at least 5 minutes old.

$pid_file = __DIR__ . DIRECTORY_SEPARATOR . 'auto_handbrake.pid';
if (file_exists($pid_file)) {
    exit("Handbrake already running\n");
}

file_put_contents($pid_file, getmypid());

$excluded_items = ['.','..'];
foreach ($results as $item){
    $full_path = $video_directory . DIRECTORY_SEPARATOR . $item;
    if (is_dir($full_path) && !in_array($item,$excluded_items) && $item != $encoded_directory){
        $item_contents = scandir($full_path);
        foreach ($item_contents as $video_file) {
            if (!in_array($video_file, $excluded_items) && determineAge($video_file, $now)) {
                $item_location = $full_path . DIRECTORY_SEPARATOR . $video_file;
                $encoded_item_directory = $video_directory . DIRECTORY_SEPARATOR . $encoded_directory . DIRECTORY_SEPARATOR . $item;
                $encoded_item_location = $encoded_item_directory . DIRECTORY_SEPARATOR . $video_file;
                if (!is_dir($encoded_item_directory)) {
                    mkdir($encoded_item_directory, 0755, True);
                }
                beginHandbrake($item_location, $encoded_item_location);
                if (file_exists($encoded_item_location)) {
                    unlink($item_location);
                }
            }
        }
    }
}

unlink($pid_file);

function determineAge($string, $now)
{
    $time_diff_in_seconds = 0;
    $string = str_replace(' - ', '-', $string);
    $string_array = explode(' ', $string);
    $string_array = array_reverse($string_array);
    $date_time = str_replace('.DVR.mp4', '', $string_array[0]);
    $date_time_array = explode('-', $date_time);
    $date = $date_time_array[0];
    $time = $date_time_array[1];
    $modified_date = str_replace('.', '-', $date);
    $modified_time = str_replace('.', ':', substr($time, 0, (strlen($time) - 3)));
    $item_date_obj = date_create_from_format('Y-m-d H:i:s', $modified_date . ' ' . $modified_time, null);
    $time_difference = $now->diff($item_date_obj);
    $time_diff_in_seconds = ($time_difference->d * 24 * 60 * 60) + ($time_difference->h * 60 * 60) +  + ($time_difference->i * 60) + $time_difference->s;
    if ($time_diff_in_seconds > 300) {
        return true;
    } else {
        return false;
    }
}

function beginHandbrake($source, $destination)
{
    // HandBrakeCLI -i /raid/video_game_clips/Cyberpunk\ 2077/Cyberpunk\ 2077\ 2020.12.10\ -\ 15.43.50.17.DVR.mp4 -o ./test.mp4 --preset="Vimeo YouTube HQ 1080p60"
    $command = '/usr/bin/HandBrakeCLI -i ' . escapeshellarg($source) . ' -o ' . escapeshellarg($destination) . ' --preset="Vimeo YouTube HQ 1080p60"';
    shell_exec($command);
}
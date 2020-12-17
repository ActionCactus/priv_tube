<?php

$apache_proxy = 'clips';
$video_directory = 'videos';
$video_full_directory = "/var/www/html/elephant" . DIRECTORY_SEPARATOR . $video_directory;

switch($_REQUEST["action"]) {
    case 'pageLoad':
        $response = pageLoad();
        break;
    default:
        $response = ["Error" => "Invalid action."];
        break;
}

echo json_encode($response);

function pageLoad()
{
    $games = getGameFolders();
    $game_clips = [];
    foreach ($games as $game) {
        $game_clips[$game] = getClips($game);
    }
    return ['games_index' => $games, 'game_clips' => $game_clips];
}

function getGameFolders()
{
    GLOBAL $video_full_directory;
    $excluded_items = ['.', '..'];
    $contents = scandir($video_full_directory);
    $games = [];
    foreach ($contents as $game) {
        if (!in_array($game, $excluded_items)) {
            $games[] = $game;
        }
    }
    return $games;
}

function getClips($game)
{
    GLOBAL $video_directory;
    GLOBAL $video_full_directory;
    GLOBAL $apache_proxy;
    $excluded_items = ['.', '..'];
    $contents = scandir($video_full_directory . DIRECTORY_SEPARATOR . $game);
    $clips = [];
    foreach ($contents as $clip) {
        if (!in_array($clip, $excluded_items)) {
            $clips[] = $clip;
        }
    }

    // Sort the clips descending so the newest are at the start of the array
    usort($clips, function($a, $b){
        $a_datetime = extractDateTime($a);
        $b_datetime = extractDateTime($b);

        if ($a_datetime == $b_datetime) {
            return 0;
        }

        return $a_datetime < $b_datetime ? 1 : -1;
    });

    foreach ($clips as $key => $clip) {
        $clips[$key] = [
            'datetime' => extractDateTime($clip)->format('Y-m-d H:i:s'),
            'src' => $apache_proxy . DIRECTORY_SEPARATOR . $video_directory . DIRECTORY_SEPARATOR . $game . DIRECTORY_SEPARATOR . $clip
        ];
    }

    return $clips;
}

function extractDateTime($clip)
{
    $string = str_replace(' - ', '-', $clip);
    $string_array = explode(' ', $string);
    $string_array = array_reverse($string_array);
    $date_time = str_replace('.DVR.mp4', '', $string_array[0]);
    $date_time_array = explode('-', $date_time);
    $date = $date_time_array[0];
    $time = $date_time_array[1];
    $modified_date = str_replace('.', '-', $date);
    $modified_time = str_replace('.', ':', substr($time, 0, (strlen($time) - 3)));
    return date_create_from_format('Y-m-d H:i:s', $modified_date . ' ' . $modified_time, null);
}

?>
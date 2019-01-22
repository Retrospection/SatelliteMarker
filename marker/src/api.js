
export function fetchInitState(url) {
    return fetch(url, {
        method: 'get'
    }).then(response => response.json())
}

export function fetchNextImage(url){

    //fetch请求
    return fetch(url,{
        method: 'get',
    }).then(response => response.json());
}

export function submitMark(url, content) {
    return fetch(url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            imageId: content.imageId,
            markValue: content.markValue
        })
    }).then(response => response.json())
}



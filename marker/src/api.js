
export function fetchImageById(url, id){
    let requestUrl
    if (url.endsWith('/')) {
        requestUrl = `${url}${id}`
    } else {
        requestUrl = `${url}/${id}`
    }
    //fetch请求
    return fetch(requestUrl,{ 
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
            mark: content
        })
    }).then(response => response.json())
}

export function fetchInitState(url) {
    return fetch(url, {
        method: 'get'
    }).then(response => response.json())
}

const serverUrl = process.env.NEXT_PUBLIC_SERVER_URL;

function objToParamString(params: Record<string, any>){
    console.log(params);
    let result = "";
    for (const [key, value] of Object.entries(params)){
        if (value){
            console.log(value, result ? "&" : "" + `${key}=${value}`)
            result += ((result ? "&" : "") + `${key}=${value}`);
        }
    }
    return result;
}


export async function send_request({
    method = "GET" as string,
    url = "" as string,
    headers = {} as Record<string, string>,
    params = {} as Record<string, any>,
    body = undefined as any,
    token = undefined as string | undefined
} = {}): Promise<any> {
    const searchParams: string = objToParamString(params);
    url = url + (searchParams ? "?" : "") + searchParams;
    const result: Response = await fetch(
        serverUrl + url,
        {
            headers: {
                "Content-Type": "application/json",
                ...((token) && { "Authorization": `Bearer ${token}` }),
                ...headers,
            },
            method: method,
            credentials: 'include',
            ...((body) && { body: JSON.stringify(body) })
        }
    );
    if (!result.ok) {
        throw new Error(`Response status: ${result.status}`);
    }

    return await result.json();
}
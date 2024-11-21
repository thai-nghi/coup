import { send_request } from "./util";

export async function registerUser(props: Record<string, any>) {
    let data = await send_request({
        method: "POST",
        url: `/auth/register`,
        body: {
            ...props
        },
    });
    return data;
}

export async function getUserInfo(token: string) {
    let data = await send_request({
        method: "GET",
        url: `/user`,
        token
    });

    return data?.data;
}

export async function sendGoogleLogin(token: string) {
    try {
        return await send_request({
            method: "POST",
            url: `/auth/login`,
            body: {
                "data": {
                    "google_token": token
                }
            }
        })
    } catch (error) {

    }
}
import RegisterForm from '@/components/register_form';
import { send_request } from '../apis/util';

export default async function Register() {

    const countries = await send_request({ method: "POST", url: "/metadata/", body: ["COUNTRY"] })
    return (
        <RegisterForm countries={countries?.COUNTRY}></RegisterForm>
    )

}
"use client";

import { Input, Checkbox, Button, Typography } from "@material-tailwind/react";
import { useGoogleLogin } from "@react-oauth/google";
import {
    useSessionStorageState,
    useRequest,
    useLocalStorageState,
} from "ahooks";
import React from "react";
// import { sendGoogleLogin } from "@/apis/user";
import registerImg from '@/assets/choi-co-up-12.jpg';

import Image from 'next/image';
import Link from "next/link";

export default function Login() {
    const [userData, setUserData] = useSessionStorageState("userData");
    const [_, setUserToken] = useSessionStorageState("googleToken");
    const [authToken, setAuthToken] = useLocalStorageState("token");

    //   const { loading: loginLoading, run: loginRun } = useRequest(sendGoogleLogin, {
    //     manual: true,
    //     onSuccess: (result, params) => {
    //       console.log(result);
    //       if (!result.has_account) {
    //         window.open("/register", "_self");
    //       } else {
    //         setUserData(result.data);
    //         setAuthToken(result.token);
    //         window.open("/profile", "_self");
    //       }
    //     },
    //     onError: (error) => {},
    //   });

    if (userData) {
        window.open("/profile", "_self");
    }

    //   const login = useGoogleLogin({
    //     onSuccess: (tokenResponse) => {
    //       setUserToken(tokenResponse.access_token);
    //       loginRun(tokenResponse.access_token);
    //     },
    //   });

    return (
        <section className="flex h-screen gap-4 p-8 bg-primary-bg">
            <div className="mt-24 w-full lg:w-3/5">
                <div className="text-center">
                    <Typography variant="h2" className="mb-4 font-bold text-white">
                        Sign In
                    </Typography>
                    <Typography
                        variant="paragraph"
                        color="blue-gray"
                        className="text-lg font-normal text-white"
                    >
                        Enter your email and password to Sign In.
                    </Typography>
                </div>
                    <form className="mx-auto mb-2 mt-8 w-80 max-w-screen-lg lg:w-1/2">

                        <div className="mb-1 flex flex-col gap-6">
                            <Typography
                                variant="small"
                                color="blue-gray"
                                className="-mb-3 font-medium text-white"
                            >
                                Your email
                            </Typography>
                            <Input
                                size="lg"
                                placeholder="name@mail.com"
                                className=" !border-white focus:!border-white text-white dark:focus:!border-white"
                                labelProps={{
                                    className: "before:content-none after:content-none",
                                }}
                            />
                            <Typography
                                variant="small"
                                color="blue-gray"
                                className="-mb-3 font-medium text-white "
                            >
                                Password
                            </Typography>
                            <Input
                                type="password"
                                size="lg"
                                placeholder="********"
                                className=" !border-white focus:border-white dark:text-white dark:focus:!border-white"
                                labelProps={{
                                    className: "before:content-none after:content-none",
                                }}
                            />
                        </div>
                        <Checkbox
                            label={
                                <Typography
                                    variant="small"
                                    color="white"
                                    className="flex items-center justify-start font-medium dark:text-slate-400"
                                >
                                    I agree the&nbsp;
                                    <a
                                        href="#"
                                        className="font-normal text-white underline transition-colors hover:text-gray-900 dark:text-white"
                                    >
                                        Terms and Conditions
                                    </a>
                                </Typography>
                            }
                            containerProps={{ className: "-ml-2.5" }}
                        />
                        <Button
                            className="mt-6 dark:bg-white dark:text-slate-900 dark:shadow-slate-900/50"
                            fullWidth
                        >
                            Sign In
                        </Button>

                        <div className="mt-6 flex items-center justify-between gap-2">
                            {/* <Checkbox
              label={
                <Typography
                  variant="small"
                  color="gray"
                  className="flex items-center justify-start font-medium dark:text-white"
                >
                  Subscribe me to newsletter
                </Typography>
              }
              containerProps={{ className: "-ml-2.5" }}
            /> */}
                            <Typography variant="small" className="font-medium text-white">
                                <Link href="/register">No account? Register now!</Link>
                            </Typography>
                            <Typography variant="small" className="font-medium text-white">
                                <a href="#">Forgot Password</a>
                            </Typography>
                        </div>
                        {/* <div className="mt-8 space-y-4">
            <Button
              size="lg"
              color="white"
              className="flex items-center justify-center gap-2 shadow-md"
              fullWidth
            >
              <svg
                width="17"
                height="16"
                viewBox="0 0 17 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g clipPath="url(#clip0_1156_824)">
                  <path
                    d="M16.3442 8.18429C16.3442 7.64047 16.3001 7.09371 16.206 6.55872H8.66016V9.63937H12.9813C12.802 10.6329 12.2258 11.5119 11.3822 12.0704V14.0693H13.9602C15.4741 12.6759 16.3442 10.6182 16.3442 8.18429Z"
                    fill="#4285F4"
                  />
                  <path
                    d="M8.65974 16.0006C10.8174 16.0006 12.637 15.2922 13.9627 14.0693L11.3847 12.0704C10.6675 12.5584 9.7415 12.8347 8.66268 12.8347C6.5756 12.8347 4.80598 11.4266 4.17104 9.53357H1.51074V11.5942C2.86882 14.2956 5.63494 16.0006 8.65974 16.0006Z"
                    fill="#34A853"
                  />
                  <path
                    d="M4.16852 9.53356C3.83341 8.53999 3.83341 7.46411 4.16852 6.47054V4.40991H1.51116C0.376489 6.67043 0.376489 9.33367 1.51116 11.5942L4.16852 9.53356Z"
                    fill="#FBBC04"
                  />
                  <path
                    d="M8.65974 3.16644C9.80029 3.1488 10.9026 3.57798 11.7286 4.36578L14.0127 2.08174C12.5664 0.72367 10.6469 -0.0229773 8.65974 0.000539111C5.63494 0.000539111 2.86882 1.70548 1.51074 4.40987L4.1681 6.4705C4.8001 4.57449 6.57266 3.16644 8.65974 3.16644Z"
                    fill="#EA4335"
                  />
                </g>
                <defs>
                  <clipPath id="clip0_1156_824">
                    <rect
                      width="16"
                      height="16"
                      fill="white"
                      transform="translate(0.5)"
                    />
                  </clipPath>
                </defs>
              </svg>
              <span>Sign in With Google</span>
            </Button>
          </div> */}
                    </form>
            </div>
            <div className="fixed right-0 top-0 hidden h-screen w-2/5 text-center content-center lg:block">
                <Image src={registerImg} alt="">

                </Image>
            </div>
        </section>
    );
}

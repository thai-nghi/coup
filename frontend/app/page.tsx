import Landing from "@/components/landing";
import Link from "next/link";
export default function Home() {
  return (
    <>
      <div className="bg-fourth-element h-10 flex flex-row justify-between">
        <div className="w-24 h-full px-5 "><Link href="/" className="w-24 h-full flex"><p className="bold text-3xl text-third-element">Coup</p></Link></div>
        <div className="w-24 h-full bg-third-element flex "><Link href="/login" className="w-24 h-full flex text-center justify-center"><p className="bold text-2xl">Login</p></Link></div>
      </div>
      <div className="relative flex h-screen content-center items-center justify-center pb-32 pt-8 bg-primary-bg">
        <div className="container flex mx-auto bg-primary-element rounded-md h-full pb-32 pt-8 ">
          <Landing></Landing>
        </div>
      </div>
    </>
  );
}

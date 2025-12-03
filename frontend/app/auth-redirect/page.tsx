"use client";

import { useSearchParams } from "next/navigation";

export default function AuthRedirectPage() {
  const searchParams = useSearchParams();
  console.log("Search params:", Array.from(searchParams.entries()));

  return <></>;
}

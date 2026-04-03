import { NextResponse } from 'next/server';

export async function GET() {
  const res = await fetch('http://localhost:8001/api/connections/');
  const data = await res.json();
  return NextResponse.json(data);
}

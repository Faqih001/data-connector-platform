import { NextResponse } from 'next/server';

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  const res = await fetch(`http://localhost:8001/api/files/${params.id}/submit_data/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data);
}

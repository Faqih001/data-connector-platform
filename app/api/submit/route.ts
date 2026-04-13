import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const body = await request.json();
  const { fileId, data } = body;
  const res = await fetch(`http://localhost:8001/api/files/${fileId}/submit_data/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data }),
  });
  const result = await res.json();
  return NextResponse.json(result);
}

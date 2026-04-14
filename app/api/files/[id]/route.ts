import { NextResponse } from 'next/server';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const res = await fetch(`http://localhost:8001/api/files/${id}/`);
  const data = await res.json();
  return NextResponse.json(data);
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const res = await fetch(`http://localhost:8001/api/files/${id}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data);
}

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const res = await fetch(`http://localhost:8001/api/files/${id}/`, {
    method: 'DELETE',
  });
  
  if (res.status === 204) {
    return NextResponse.json({ success: true }, { status: 204 });
  }
  
  const data = await res.json();
  return NextResponse.json(data);
}

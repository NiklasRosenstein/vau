from vau.reflection import Reflection


def test_reflection_into_behaves_different_than_wrapped_object():
    class A:
        def foo(self, a: int = 1) -> int:
            return a

    a = A()
    refl = Reflection(a)
    refl.method("foo").kwargs["a"] = 2
    b = refl.into(A)

    assert a.foo() == 1
    assert b.foo() == 2

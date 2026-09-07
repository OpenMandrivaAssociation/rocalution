# Iterative sparse solvers. TheRock 10.0.

Name:		rocalution
Version:	10.0.0
Release:	1
Summary:	ROCm iterative sparse solver library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.0/rocalution.tar.gz#/rocalution-%{version}.tar.gz
# HIP backend uses host symbols; a separate hip DSO cannot link with --no-undefined
Patch0:		0001-fold-hip-objects-into-librocalution.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	rocsparse-devel
BuildRequires:	rocblas-devel
BuildRequires:	rocprim-devel
BuildRequires:	cmake(rocrand)
BuildRequires:	openmp-devel
BuildRequires:	cmake(AMDDeviceLibs)
BuildRequires:	clang >= %{rocm_llvm_maj_ver}

%description
rocALUTION is a sparse iterative solver library with HIP and
host backends.

%package devel
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for rocALUTION.

%prep
%autosetup -n rocalution -p1

%build
export CXX=hipcc
export CC=clang
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DOpenMP_CXX_FLAGS=-fopenmp \
	-DOpenMP_CXX_LIB_NAMES=omp \
	-DOpenMP_omp_LIBRARY=%{_libdir}/libomp.so \
	-DCMAKE_HIP_COMPILER=clang++ \
	-DCMAKE_HIP_FLAGS="--rocm-path=%{_prefix} --rocm-device-lib-path=%{_libdir}/amdgcn/bitcode" \
	-DCMAKE_HIP_ARCHITECTURES="%{rocm_gpu_targets}" \
	-DUSE_HIPCXX=ON \
	-DSUPPORT_HIP=ON \
	-DSUPPORT_MPI=OFF \
	-DBUILD_CLIENTS_TESTS=OFF \
	-DBUILD_CLIENTS_BENCHMARKS=OFF \
	-DBUILD_CLIENTS_SAMPLES=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
rm -f %{buildroot}%{_docdir}/rocalution/LICENSE.md

%files
%license LICENSE.md
%doc README.md
%{_libdir}/librocalution.so.*

%files devel
%{_includedir}/rocalution/
%{_libdir}/librocalution.so
%{_libdir}/cmake/rocalution/
